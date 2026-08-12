"""
Rewrite embedded data URIs in a notebook into repository raw URLs.

    python tools/rewrite_data_uris.py notebooks/Week01.ipynb

Every <img src="data:image/svg+xml;base64,..."> is decoded and matched byte-for-byte
against the files in img/. A match is replaced with its raw URL. An unmatched image is
reported and left alone, so nothing is silently lost.
"""

import base64, json, os, re, sys

USER, REPO, BRANCH = "youngkorea", "ai-programming-fundamentals", "main"
RAW = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/img/"
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "img")

PATTERN = re.compile(r'data:image/svg\+xml;base64,([A-Za-z0-9+/=]+)')


def load_index():
    index = {}
    for name in os.listdir(IMG_DIR):
        if name.endswith(".svg"):
            with open(os.path.join(IMG_DIR, name), encoding="utf-8") as f:
                index[f.read().strip()] = name
    return index


def main(path):
    index = load_index()
    nb = json.load(open(path, encoding="utf-8"))
    replaced = missed = 0

    def sub(match):
        nonlocal replaced, missed
        try:
            body = base64.b64decode(match.group(1)).decode("utf-8").strip()
        except Exception:
            missed += 1
            return match.group(0)
        name = index.get(body)
        if not name:
            missed += 1
            print("  ! no match in img/ for one embedded image; left as a data URI")
            return match.group(0)
        replaced += 1
        print(f"  -> {name}")
        return RAW + name

    for cell in nb["cells"]:
        cell["source"] = [PATTERN.sub(sub, line) for line in cell["source"]]

    json.dump(nb, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{replaced} replaced, {missed} left untouched -> {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: python tools/rewrite_data_uris.py <notebook.ipynb>")
    main(sys.argv[1])
