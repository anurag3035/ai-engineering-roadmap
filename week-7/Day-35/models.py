from dataclasses import dataclass, field


@dataclass
class Document:

    id: str

    content: str

    embedding: list[float] = field(
        default_factory=list
    )

    metadata: dict = field(
        default_factory=dict
    )