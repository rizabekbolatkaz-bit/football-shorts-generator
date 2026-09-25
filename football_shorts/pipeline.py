import json
from pathlib import Path
from .detector import detect_candidates, save_events
from .selector import select_for_duration
from .render import render_short

def build_short(video: Path, output_dir: Path, target_s: float = 75.0) -> Path:
    if not video.exists():
        raise FileNotFoundError(video)
    output_dir.mkdir(parents=True, exist_ok=True)
    candidates = detect_candidates(video)
    selected = select_for_duration(candidates, target_s)
    save_events(candidates, output_dir / "events.json")
    (output_dir / "selected_events.json").write_text(
        json.dumps([e.to_dict() for e in selected], indent=2), encoding="utf-8")
    if not selected:
        raise RuntimeError("No candidate events detected")
    return render_short(video, selected, output_dir / "short.mp4")
