from dataclasses import dataclass, asdict


@dataclass
class Option:
    type: int
    name: str # 1-32
    description: str
    required: bool
    empty: bool
    def __post_init__(self):
        if self.required is None:
            self.required = False
        if self.empty is None:
            self.empty = False
    def dict(self):
        if self.empty:
            return {}
        return {k: str(v) for k,v in asdict(self).items()}