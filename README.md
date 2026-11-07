# AEVORIN — Independent AI Research & Engineering

Static site (EN at `/`, KO at `/ko/`). Numbers come from `data/research.json`, which `tools/extract.py` generates from source analysis files.
Page text lives in `tools/content.py`; `tools/build.py` renders the pages and subsets the fonts.

```bash
python3 -I tools/extract.py /path/to/Nexus-.github.io     # regenerate data/research.json
FONT_SRC=/path/to/ttf python3 -I tools/build.py            # build pages + fonts (--no-fonts to skip fonts)
python3 -I -m unittest discover -s tests -v                # forbidden-string scan, link check, number-to-data check
python3 -m http.server 8000                                # preview
```

Fonts (OFL): Cormorant Garamond, Inter, Noto Serif KR, Noto Sans KR. Source TTFs are not stored here; `build.py` subsets them to the characters the site uses.
Hand-verified figures (Phase 2b, Study 4, LLM test counts) are marked `verified` in the data file.
