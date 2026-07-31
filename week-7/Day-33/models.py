from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Document:
    id: str
    content: str
    embedding: list[float]
    metadata: Dict[str, str] = field(default_factory=dict)