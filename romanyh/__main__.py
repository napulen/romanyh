import argparse
import os
import romanyh
from music21.pitch import Pitch


def valid_voicing(s):
    """Verifies a string of 4 space-separated pitches as a valid voicing."""
    pitchStrings = s.split()
    if len(pitchStrings) != 4:
        msg = "The voicing should have exactly 4 notes"
        raise argparse.ArgumentTypeError(msg)
    b, t, a, s = [Pitch(p) for p in pitchStrings]
    if not b <= t <= a <= s:
        msg = "The notes of the given voicing should be ordered BTAS"
        raise argparse.ArgumentTypeError(msg)
    return tuple(pitchStrings)


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
    parser.add_argument(
        "--close-position",
        action="store_true",
        help="Voice in close position (tenor and soprano within one octave)",
    )
    parser.add_argument(
        "--tonic",
        type=str,
        default=None,
        metavar="TONIC",
        help="Transpose the RomanText file to a new tonic",
    )
    parser.add_argument(
        "--first-voicing",
        type=valid_voicing,
        help="Fix the first voicing to something of your liking",
    )
    parser.add_argument(
        "--last-voicing",
        type=valid_voicing,
        help="Fix the last voicing to something of your liking",
    )

    args = parser.parse_args()
    for i, score in enumerate(
        romanyh.harmonizations(
            args.input,
            args.close_position,
            args.tonic,
            args.first_voicing,
            args.last_voicing,
        )
    ):
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
