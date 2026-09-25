from pathlib import Path
import argparse
from football_shorts.pipeline import build_short

def main():
    p = argparse.ArgumentParser(description="Full football match -> one highlight Short")
    p.add_argument("input", type=Path, help="Local full-match video")
    p.add_argument("--output", type=Path, default=Path("out"))
    p.add_argument("--target", type=float, default=75.0, help="Target short duration in seconds")
    args = p.parse_args()
    result = build_short(args.input, args.output, args.target)
    print(result)

if __name__ == "__main__":
    main()
