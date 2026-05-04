#!/usr/bin/env python3
from argparse import ArgumentParser
import re
from pathlib import Path
import csv
from pypdf import PdfReader


def fmt_author(s):
    if s.endswith(" 著") or s.endswith(" 作") or s.endswith(" 編"):
        s = s[:-2]
    if s == "森鴎外" or s == "森林太郎":
        s = "森鷗外"
    return s


def fmt_title(s, k):
    if k.startswith("国訳大蔵経編輯部 編『国訳大蔵経 : 昭和新纂』宗典部"):
        s = "昭和新纂國譯大藏經宗典部"
    return s


def kanji_to_int(s: str) -> int:
    kanji_map = {
        "一": 1,
        "二": 2,
        "三": 3,
        "四": 4,
        "五": 5,
        "六": 6,
        "七": 7,
        "八": 8,
        "九": 9,
    }
    num = 0
    tmp = 0
    for c in s:
        if c == "十":
            tmp = max(tmp, 1) * 10
            num += tmp
            tmp = 0
        elif c in kanji_map:
            tmp = tmp * 10 + kanji_map[c]
    return num + tmp


def parse_number(v: str) -> int:
    # 全角→半角
    v = v.translate(str.maketrans("０１２３４５６７８９", "0123456789"))
    if v.isdigit():
        return int(v)
    return kanji_to_int(v)


def get_volume(s: str) -> int:
    m = re.search(r"第([0-9０-９一二三四五六七八九十]+)巻", s)
    if m:
        return parse_number(m.group(1))

    m = re.search(r"〔第([0-9０-９一二三四五六七八九十]+)〕", s)
    if m:
        return parse_number(m.group(1))

    return 1


def main():
    parser = ArgumentParser()
    parser.add_argument("infiles", nargs="+")
    parser.add_argument("--csv", default="ndl.csv")
    args = parser.parse_args()
    pids = set()

    with open(args.csv, mode="w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PID", "Author", "Title", "Vol", "File", "Keywords"])

        for file in args.infiles:
            reader = PdfReader(file)
            meta = reader.metadata
            if meta is None:
                continue
            k = meta.get("/Keywords")
            if not k:
                continue
            m = re.search(r"pid/(\d+)", k)
            if not m:
                continue
            pid = m.group(1)
            if pid in pids:
                continue
            pids.add(pid)
            author = meta.get("/Author")
            title = meta.get("/Title")
            author = fmt_author(author)
            title = fmt_title(title, k)
            vol = get_volume(k)
            k = k.split("国立国会図書館")[0]
            f = Path(file).stem
            writer.writerow([pid, author, title, vol, f, k])
            print(pid, author, title, vol, k)


if __name__ == "__main__":
    main()
