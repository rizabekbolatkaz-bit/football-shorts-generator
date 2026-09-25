import subprocess
from pathlib import Path
from .models import Event

def render_short(video: Path, events: list[Event], output: Path) -> Path:
    work = output.parent / "_parts"
    work.mkdir(parents=True, exist_ok=True)
    parts = []
    for i, e in enumerate(events):
        part = work / f"{i:03d}.mp4"
        vf = "scale=-2:1920,crop=1080:1920"
        subprocess.run([
            "ffmpeg","-y","-v","error","-ss",str(e.start),"-to",str(e.end),"-i",str(video),
            "-vf",vf,"-c:v","libx264","-preset","veryfast","-crf","20",
            "-c:a","aac","-ar","48000",str(part)
        ], check=True)
        parts.append(part)
    concat = work / "concat.txt"
    concat.write_text("\n".join(f"file '{p.resolve().as_posix()}'" for p in parts), encoding="utf-8")
    subprocess.run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(concat),
                    "-c","copy",str(output)], check=True)
    return output
