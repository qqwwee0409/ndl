#!/usr/bin/env python3
import argparse
import pyperclip
from opencc import OpenCC


def get_map(args):
    def_map = {}
    if args.modest > 0:
        def_map["才"] = "才"
        def_map["連"] = "連"
        def_map["聡"] = "聡"
        def_map["却"] = "却"
        def_map["灯"] = "灯"
        def_map["闘"] = "闘"
        def_map["峰"] = "峰"
        def_map["氷"] = "氷"
        def_map["疏"] = "疏"
        def_map["粧"] = "粧"
        def_map["唇"] = "唇"
        def_map["猫"] = "猫"
        def_map["煙"] = "煙"
        def_map["群"] = "群"
        def_map["醋"] = "醋"
        def_map["呪"] = "呪"
        def_map["恒"] = "恒"
        def_map["兎"] = "兎"
        def_map["脚"] = "脚"
        def_map["讬"] = "託"
        def_map["涜"] = "瀆"
        def_map["即"] = "卽"
        def_map["益"] = "益"
        def_map["腳"] = "脚"
        def_map["兔"] = "兎"
        def_map["眾"] = "衆"
        def_map["屡"] = "屢"
        def_map["篭"] = "籠"
        def_map["蝉"] = "蟬"
        def_map["真"] = "眞"
        def_map["姉"] = "姊"
        def_map["恆"] = "恒"
        def_map["清"] = "淸"
        def_map["青"] = "靑"
        def_map["視"] = "視"
        def_map["神"] = "神"
        def_map["祖"] = "祖"
        def_map["福"] = "福"
        def_map["祈"] = "祈"
        def_map["遥"] = "遙"
        def_map["遙"] = "遙"
        def_map["予"] = "予"
        def_map["双"] = "双"
        def_map["効"] = "効"
        def_map["床"] = "床"
        def_map["弁"] = "弁"
        def_map["勅"] = "勅"
        def_map["稜"] = "稜"
        def_map["汚"] = "汚"
        def_map["岳"] = "岳"
        def_map["缶"] = "缶"
        # def_map["敕"] = "勅"
    if args.modest > 1:
        def_map["糸"] = "糸"
        def_map["余"] = "余"
        def_map["欠"] = "欠"
    if args.modest > 2:
        def_map["台"] = "台"
        def_map["条"] = "条"
        def_map["痴"] = "痴"
    return def_map


def small_to_large_kana(text: str) -> str:
    table = str.maketrans(
        {
            "ぁ": "あ",
            "ぃ": "い",
            "ぅ": "う",
            "ぇ": "え",
            "ぉ": "お",
            "っ": "つ",
            "ゃ": "や",
            "ゅ": "ゆ",
            "ょ": "よ",
            "ゎ": "わ",
            "ゕ": "か",
            "ゖ": "け",
            "ァ": "ア",
            "ィ": "イ",
            "ゥ": "ウ",
            "ェ": "エ",
            "ォ": "オ",
            "ッ": "ツ",
            "ャ": "ヤ",
            "ュ": "ユ",
            "ョ": "ヨ",
            "ヮ": "ワ",
            "ヵ": "カ",
            "ヴ": "ブ",
            #  'ヶ': 'ケ',
        }
    )
    return text.translate(table)


def small_to_large_kan2a(text: str) -> str:
    table = str.maketrans(
        {
            "ぁ": "あ",
            "ぃ": "い",
            "ぅ": "う",
            "ぇ": "え",
            "ぉ": "お",
            "っ": "つ",
            "ゃ": "や",
            "ゅ": "ゆ",
            "ょ": "よ",
            "ゎ": "わ",
            "ゕ": "か",
            "ゖ": "け",
        }
    )
    return text.translate(table)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="clip")
    parser.add_argument("--copy", action="store_true")
    parser.add_argument("--hira", action="store_true")
    parser.add_argument("--modest", type=int, default=0)
    parser.add_argument("--diff", action="store_true")
    parser.add_argument("--daiji", action="store_true")
    args = parser.parse_args()

    cc = OpenCC("jp2t")
    user_map = get_map(args)
    # for k, v in user_map.items():
    #     if k == v:
    #         print(k, cc.convert(k))
    # exit()

    if args.input == "clip":
        text = pyperclip.paste().strip()
    else:
        with open(args.input, encoding="utf8") as f:
            text = f.read()
    if not text:
        print("ERROR: input is empty!")
        return
    if args.hira:
        result = []
        for ch in text:
            code = ord(ch)
            if 0x3041 <= code <= 0x3096:
                result.append(chr(code + 0x60))
            else:
                result.append(ch)
        text = "".join(result)

    user_map = get_map(args)
    converted = ""
    for c in text:
        if (char := user_map.get(c)) is None:
            char = cc.convert(c)
        converted += char
    if args.daiji:
        converted = small_to_large_kana(converted)
    print(converted)

    if args.copy:
        pyperclip.copy(converted)
        print("\n[clipboard updated]")

    if args.diff:
        print("\n--- Changes ---")
        changes = []
        for original_char, converted_char in zip(text, converted):
            if original_char != converted_char:
                diff_str = f"{original_char} -> {converted_char}"
                if diff_str not in changes:
                    changes.append(diff_str)

        if changes:
            print("\n".join(changes))
        else:
            print("No changes found.")


if __name__ == "__main__":
    main()
