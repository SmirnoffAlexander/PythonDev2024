#!/usr/bin/env python
import argparse

import cowsay


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("message", nargs="*", default="", type=str)
    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-e", "--eye_string", default="OO", type=str)
    parser.add_argument("-f", "--cowfile", default="default", type=str)
    parser.add_argument("-n", action="store_true")
    parser.add_argument("-W", "--width", default=40, type=int)
    parser.add_argument("-T", "--tongue_string", default="  ", type=str)
    parser.add_argument("-b", action="store_true")
    parser.add_argument("-d", action="store_true")
    parser.add_argument("-g", action="store_true")
    parser.add_argument("-p", action="store_true")
    parser.add_argument("-s", action="store_true")
    parser.add_argument("-t", action="store_true")
    parser.add_argument("-w", action="store_true")
    parser.add_argument("-y", action="store_true")

    args = parser.parse_args()
    preset_str = "bdgpstwy"
    preset = None

    best_ind = 0
    for arg in vars(args):
        if arg in preset_str and getattr(args, arg):
            best_ind = preset_str.index(arg)
            preset = preset_str[best_ind]

    if args.list is True:
        print(cowsay.list_cows())
        return

    if not len(args.message):
        raise RuntimeError("Message is empty")

    kwargs = {
        "message": " ".join(args.message),
        "eyes": args.eye_string,
        "cow": args.cowfile,
        "width": args.width,
        "preset": preset,
        "tongue": args.tongue_string,
        "wrap_text": args.n,
    }
    print(cowsay.cowsay(**kwargs))


if __name__ == "__main__":
    main()
