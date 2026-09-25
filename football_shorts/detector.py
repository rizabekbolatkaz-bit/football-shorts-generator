import json
import subprocess
from pathlib import Path
import numpy as np
from .models import Event

def _audio_pcm(video: Path, rate: int = 8000) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-i", str(video), "-vn", "-ac", "1",
           "-ar", str(rate), "-f", "s16le", "pipe:1"]
    raw = subprocess.check_output(cmd)
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0

def detect_candidates(video: Path, window_s: float = 2.0, min_gap_s: float = 12.0) -> list[Event]:
    """Cheap first pass: crowd/commentary audio peaks generate candidate moments."""
    rate = 8000
    audio = _audio_pcm(video, rate)
    n = max(1, int(rate * window_s))
    usable = audio[: len(audio) // n * n]
    if not len(usable):
        return []
    rms = np.sqrt(np.mean(usable.reshape(-1, n) ** 2, axis=1) + 1e-12)
    threshold = float(np.quantile(rms, 0.90))
    order = np.argsort(rms)[::-1]
    picked = []
    for idx in order:
        t = (float(idx) + 0.5) * window_s
        if rms[idx] < threshold:
            break
        if all(abs(t - e.timestamp) >= min_gap_s for e in picked):
            picked.append(Event(t, max(0.0, t - 5.0), t + 6.0, float(rms[idx]), confidence=0.25))
    return sorted(picked, key=lambda e: e.timestamp)

def save_events(events: list[Event], path: Path):
    path.write_text(json.dumps([e.to_dict() for e in events], indent=2), encoding="utf-8")
