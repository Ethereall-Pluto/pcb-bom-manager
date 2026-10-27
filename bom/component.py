from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Component:
    """A single part placed on a PCB, identified by its reference designator (R1, C3, U2)."""

    designator: str
    value: str
    footprint: str
    unit_price: Decimal

    def __post_init__(self) -> None:
        if not self.designator.strip():
            raise ValueError("designator must not be empty")
        if self.unit_price < 0:
            raise ValueError(f"{self.designator}: unit_price must be >= 0, got {self.unit_price}")

    @property
    def part_key(self) -> tuple[str, str]:
        """Parts with the same value and footprint are the same purchasable item."""
        return (self.value, self.footprint)
