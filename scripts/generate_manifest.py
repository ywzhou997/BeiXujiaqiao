#!/usr/bin/env python3
import os
import re
import json

PERIOD_ORDER = [
    "PeriodII", "PeriodII-III", "PeriodIII", "PeriodIII-IVEarly", "PeriodIII-IVLate",
    "PeriodIV", "PeriodIVEarly", "PeriodIVEarly-IVLate", "PeriodIVLate",
    "PeriodIVEarly-EarlyWZ", "PeriodEarlyWZ", "PeriodShang", "PeriodShang-ZhouTransition",
    "PeriodShangZhou", "PeriodSuiTang", "PeriodSongYuan", "Unperiodized", "recent",
]

TYPE_KEYWORDS = [
    "muzang", "huikeng", "daogou", "gou", "keng", "jing", "lu", "jiao", "jisi", "sanshui",
    "hangtuqiang", "hangtugoucao", "hongshaotu", "huozao", "wengguanzang", "mutan", "zhuchu",
    "zhuji", "zhudong", "chezhe", "lumian", "shaotumian", "jar", "zao", "dongwutaiji",
    "nanwutaiji", "xiwutaiji", "huangtuaogou", "huigou",
]

DIR_META = {
    "T2": (None, ["T2"]),
    "T3": (None, ["T3"]),
    "T4 Compound II": ("Compound II", ["T4"]),
    "T5": (None, ["T5"]),
    "T5 Compound VIII": ("Compound VIII", ["T5"]),
    "T5 Compound IX": ("Compound IX", ["T5"]),
    "T7": (None, ["T7"]),
    "T8": (None, ["T8"]),
    "T9 Compound IV": ("Compound IV", ["T9"]),
    "T10": (None, ["T10"]),
    "T11 T12 Compound VI": ("Compound VI", ["T11", "T12"]),
    "T13 Compound I": ("Compound I", ["T13"]),
    "T14 T15 Compound VII": ("Compound VII", ["T14", "T15"]),
    "T16": (None, ["T16"]),
    "T17 Compound III": ("Compound III", ["T17"]),
    "T18": (None, ["T18"]),
    "T19": (None, ["T19"]),
    "T20 Compound V": ("Compound V", ["T20"]),
    "T21T22": (None, ["T21", "T22"]),
    "T23": (None, ["T23"]),
    "T24": (None, ["T24"]),
}


def classify_file(filename):
    base = filename.replace(".geojson", "")
    if re.search(r"interpretation", filename, re.I):
        return {"featureType": "interpretation", "period": None, "isBase": False, "isInterpretation": True}

    if re.match(r"^(T\d+|Compound[A-Z]+)\.geojson$", filename):
        return {"featureType": "base", "period": None, "isBase": True, "isInterpretation": False}

    period = None
    for p in sorted(PERIOD_ORDER, key=len, reverse=True):
        if f"_{p}_" in base or base.endswith(f"_{p}"):
            period = p
            break

    suffix = base
    if period:
        marker = f"_{period}_"
        if marker in base:
            suffix = base[base.index(marker) + len(marker):]
        elif base.endswith(f"_{period}"):
            suffix = ""

    if re.search(r"^F\d+", suffix) or suffix == "foundation" or suffix.endswith("_foundation") or suffix.startswith("foundation_"):
        ft = "foundation"
    else:
        ft = "other"
        lower = suffix.lower()
        for kw in sorted(TYPE_KEYWORDS, key=len, reverse=True):
            if kw in lower:
                ft = kw
                break
        if ft == "other" and lower.endswith("foundation"):
            ft = "foundation"

    return {"featureType": ft, "period": period, "isBase": False, "isInterpretation": False}


def main():
    manifest = []
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for dir_name in sorted(os.listdir(root)):
        if not dir_name.startswith("T") or not os.path.isdir(os.path.join(root, dir_name)):
            continue
        if dir_name in DIR_META:
            compound, trenches = DIR_META[dir_name]
        else:
            compound = None
            m = re.search(r"Compound ([IVXLC]+)", dir_name)
            if m:
                compound = f"Compound {m.group(1)}"
            ts = re.findall(r"T(\d+)", dir_name)
            trenches = [f"T{t}" for t in ts] if ts else [dir_name.split()[0]]

        files = []
        for f in sorted(os.listdir(os.path.join(root, dir_name))):
            if f.endswith(".geojson"):
                files.append({"name": f, **classify_file(f)})

        if files:
            manifest.append({
                "dir": dir_name,
                "compound": compound,
                "trenches": trenches,
                "files": files,
            })

    out_path = os.path.join(root, "manifest.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
    print(f"Wrote {out_path}: {len(manifest)} dirs, {sum(len(m['files']) for m in manifest)} files")


if __name__ == "__main__":
    main()
