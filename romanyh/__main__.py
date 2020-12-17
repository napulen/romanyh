import argparse
import os
import romanyh


def main():
    parser = argparse.ArgumentParser(
        description="Generates four-part harmony with idiomatic "
        "voice-leading procedures and dynamic programming."
    )
    parser.add_argument(
        "input",
        type=str,
        nargs="?",
        default="example.rntxt",
        help="A RomanText input file with the chord progression",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show instead of writing to disk (uses music21's show())",
    )
    parser.add_argument(
        "--output",
        type=str,
        metavar="FILE",
        help="Write output to this file (ignored when --show is selected)",
    )
    parser.add_argument(
        "--harmonizations",
        type=int,
        default=1,
        help="Generate N alternative harmonizations",
    )

    args = parser.parse_args()
    for i, score in enumerate(romanyh.harmonizations(args.input)):
        if i == args.harmonizations:
            break
        if args.show:
            score.show()
        else:
            filepath = args.output or args.input
            filename, extension = os.path.splitext(filepath)
            version = f"_v{i + 1}" if i > 0 else ""
            filepath = filename + version + ".musicxml"
            score.write(fp=filepath, fmt="musicxml")


if __name__ == "__main__":
    main()
