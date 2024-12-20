from __future__ import annotations
from dataclasses import field, dataclass
from datetime import datetime, UTC
from uuid import UUID, uuid4


def _utc_now() -> datetime:
    """Return datetime.now in UTC."""
    return datetime.now(UTC)


@dataclass(slots=True, kw_only=True)
class Node:
    """Recursive datatype."""

    id: UUID = field(default_factory=uuid4)
    nodes: list[Node] = field(default_factory=list)


@dataclass(slots=True, kw_only=True)
class Object:
    """Simple datatype."""

    node: Node
    name: str
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)
