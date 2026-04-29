#!/usr/bin/env python3
from argparse import ArgumentParser
import os
from PIL import Image

def crop_margins(input_folder, output_folder, w, h, l, t):
    """
    指定したピクセル数だけ端を切り取る
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    valid_extensions = ('.jpg', '.jpeg', '.JPG', '.JPEG')

    for filename in os.listdir(input_folder):
        if filename.endswith(valid_extensions):
            img_path = os.path.join(input_folder, filename)
            with Image.open(img_path) as img:
                width, height = img.size
                new_box = (l, t, l+w, t+h)
                print(width, height, new_box)
                cropped_img = img.crop(new_box)
                cropped_img.save(os.path.join(output_folder, filename))
            print(f"Cropped: {filename}")


def main():
    parser = ArgumentParser()
    parser.add_argument("--input", default=".")
    parser.add_argument("--output", default="tmp")
    parser.add_argument("w", type=int, default=0)
    parser.add_argument("h", type=int)
    parser.add_argument("l", type=int)
    parser.add_argument("t", type=int)
    args = parser.parse_args()
    print(args)
    os.makedirs( args.output, exist_ok=True)
    crop_margins(args.input, args.output, args.w, args.h, args.l, args.t)


if __name__ == "__main__":
    main()