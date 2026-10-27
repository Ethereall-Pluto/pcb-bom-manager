from dataclasses import dataclass
from decimal import Decimal

from bom.component import Component


@dataclass(frozen=True)
class BomLine:
    """One row of a grouped BOM: identical parts merged into a single line."""

    value: str
    footprint: str
    designators: tuple[str, ...]
    unit_price: Decimal

    @property
    def quantity(self) -> int:
        return len(self.designators)

    @property
    def line_cost(self) -> Decimal:
        return self.unit_price * self.quantity


class BOM:
    """Bill of Materials for one board: the list of components and what they cost."""

    def __init__(self, board_name: str) -> None:
        self.board_name = board_name
        self._components: dict[str, Component] = {}

    def add(self, component: Component) -> None:
        if component.designator in self._components:
            raise ValueError(f"designator {component.designator} is already on the board")
        for existing in self._components.values():
            if existing.part_key == component.part_key and existing.unit_price != component.unit_price:
                raise ValueError(
                    f"{component.designator}: price {component.unit_price} conflicts with "
                    f"{existing.designator} ({existing.unit_price}) for the same part"
                )
        self._components[component.designator] = component

    def remove(self, designator: str) -> None:
        if designator not in self._components:
            raise KeyError(f"no component with designator {designator}")
        del self._components[designator]

    def __len__(self) -> int:
        return len(self._components)

    def grouped(self) -> list[BomLine]:
        groups: dict[tuple[str, str], list[Component]] = {}
        for component in self._components.values():
            groups.setdefault(component.part_key, []).append(component)

        return [
            BomLine(
                value=value,
                footprint=footprint,
                designators=tuple(sorted(c.designator for c in parts)),
                unit_price=parts[0].unit_price,
            )
            for (value, footprint), parts in sorted(groups.items())
        ]

    def total_cost(self, boards: int = 1) -> Decimal:
        if boards < 1:
            raise ValueError(f"boards must be >= 1, got {boards}")
        return sum((line.line_cost for line in self.grouped()), Decimal("0")) * boards
