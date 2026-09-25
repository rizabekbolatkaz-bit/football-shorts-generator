from dataclasses import dataclass, asdict

@dataclass
class Event:
    timestamp: float
    start: float
    end: float
    score: float
    kind: str = "candidate"
    confidence: float = 0.0

    def to_dict(self):
        return asdict(self)
