from .models import Event

def dedupe(events: list[Event], gap: float = 14.0) -> list[Event]:
    ranked = sorted(events, key=lambda e: e.score, reverse=True)
    kept = []
    for event in ranked:
        if all(abs(event.timestamp - x.timestamp) >= gap for x in kept):
            kept.append(event)
    return kept

def select_for_duration(events: list[Event], target_s: float) -> list[Event]:
    events = dedupe(events)
    selected, total = [], 0.0
    for e in sorted(events, key=lambda x: x.score, reverse=True):
        duration = e.end - e.start
        if selected and total + duration > target_s:
            continue
        selected.append(e)
        total += duration
        if total >= target_s * 0.9:
            break
    return sorted(selected, key=lambda e: e.timestamp)
