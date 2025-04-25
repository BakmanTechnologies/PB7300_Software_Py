#!/usr/bin/env python3

import argparse
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Skeleton Python CLI tool"
    )
    parser.add_argument(
        "-s", "--scan",
        action="store_true",
        help="Start a scan"
    )
    parser.add_argument(
        "-d", "--dwell",
        type=str,
        default="no-scan",
        help="Start a dwell"
    )
    parser.add_argument(
        "-sta", "--start",
        type=int,
        default=1300,
        help="Scan start frequency in GHz"
    )
    parser.add_argument(
        "-sto", "--stop",
        type=int,
        default=1320,
        help="Scan stop frequency in GHz"
    )
    parser.add_argument(
        "-ste", "--step",
        type=int,
        default=1,
        help="Scan step size in GHz"
    )
    parser.add_argument(
        "-tc", "--time",
        type=int,
        default=100,
        help="Time constant in ms"
    )

    # Dwell Parameters
    # Target Freq GHz
    # Time Constant
    # # of Points
    # Modulation Voltage

    # Ability to pass in COM port

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if args.verbose:
        print(f"Scan: {args.scan}")
        print(f"Start Freq: {args.start} GHz")
        print(f" Stop Freq: {args.stop} GHz")
        print(f" Step Freq: {args.step} GHz")
        print(f"Time Const: {args.time} ms")


if __name__ == "__main__":
    main()
