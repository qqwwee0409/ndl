#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import defaultdict
import os
import pyperclip
# import unidic
import MeCab


def extract_words(text):
    raw_path = "~/dic/unidic-qkana-v202512"
    dic_path = os.path.expanduser(raw_path)
    tagger = MeCab.Tagger(f"-d {dic_path}")
    # tagger = MeCab.Tagger(f'-d {unidic.DICDIR}')
    # tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    word_list = []
    errors = set()
    dic = defaultdict(lambda: defaultdict(int))
    while node:
        if not node.surface:
                    node = node.next
                    continue
        features = node.feature.split(',')
        pos = features[0]  # 品詞
        dic[pos][node.surface] += 1
        node = node.next
    return dic


def main():
    parser = ArgumentParser()
    parser.add_argument("--input", default="clip")
    args = parser.parse_args()
    if args.input == "clip":
        text = pyperclip.paste().strip()
    else:
        with open(args.input, encoding="utf8") as f:
            text = f.read()
    dic = extract_words(text)
    print(text)
    for k, v in dic.items():
         print(k)
         print(v)


if __name__ == "__main__":
    main()