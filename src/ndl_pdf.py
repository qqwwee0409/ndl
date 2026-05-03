#!/usr/bin/env python3
from argparse import ArgumentParser
import re
import csv
from pypdf import PdfReader


def main():
    parser = ArgumentParser()
    parser.add_argument("infiles", nargs="+")
    parser.add_argument("--csv", default="ndl.csv")
    args = parser.parse_args()

    with open(args.csv, mode="w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PID", "Author", "Title", "Keywords"])

        for file in args.infiles:
            reader = PdfReader(file)
            meta = reader.metadata
            if meta is None:
                print("no meta", file)
                continue
            k = meta.get("/Keywords")
            if not k:
                continue
            m = re.search(r"pid/(\d+)", k)
            if not m:
                continue
            pid = m.group(1)
            author = meta.get("/Author")
            title = meta.get("/Title")
            keywords = k  # /Keywords
            writer.writerow([pid, author, title, keywords])
            print(f"追加完了: {pid} - {title}")


if __name__ == "__main__":
    main()
