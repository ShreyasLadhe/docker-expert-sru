from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
import uuid

@dataclass
class Todo:
    id: str
    title: str
    done: bool
    created_at: str 

    @staticmethod
    def new(title: str) -> "Todo":
        return Todo(
            id=str(uuid.uuid4()),
            title=title.strip(),
            done=False,
            created_at=datetime.utcnow().isoformat()
        )

    def to_dict(self):
        return asdict(self)
