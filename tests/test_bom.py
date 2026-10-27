import csv
from decimal import Decimal

import pytest

from bom import BOM, BomExporter, Component


def resistor(designator: str, price: str = "0.02") -> Component:
    return Component(designator, "10k", "0805", Decimal(price))


def test_component_rejects_negative_price():
    with pytest.raises(ValueError):
        Component("R1", "10k", "0805", Decimal("-1"))


def test_component_rejects_empty_designator():
    with pytest.raises(ValueError):
        Component("  ", "10k", "0805", Decimal("0.02"))


def test_add_rejects_duplicate_designator():
    bom = BOM("test")
    bom.add(resistor("R1"))
    with pytest.raises(ValueError):
        bom.add(resistor("R1"))


def test_add_rejects_conflicting_price_for_same_part():
    bom = BOM("test")
    bom.add(resistor("R1", "0.02"))
    with pytest.raises(ValueError):
        bom.add(resistor("R2", "0.05"))


def test_remove_unknown_designator_raises():
    with pytest.raises(KeyError):
        BOM("test").remove("R99")


def test_grouped_merges_identical_parts():
    bom = BOM("test")
    bom.add(resistor("R2"))
    bom.add(resistor("R1"))
    bom.add(Component("C1", "100n", "0603", Decimal("0.03")))

    lines = bom.grouped()

    assert len(lines) == 2
    resistor_line = next(line for line in lines if line.value == "10k")
    assert resistor_line.designators == ("R1", "R2")
    assert resistor_line.quantity == 2


def test_total_cost_scales_with_board_count():
    bom = BOM("test")
    bom.add(resistor("R1"))
    bom.add(resistor("R2"))
    bom.add(Component("U1", "NE555", "SOIC-8", Decimal("0.40")))

    assert bom.total_cost() == Decimal("0.44")
    assert bom.total_cost(boards=10) == Decimal("4.40")


def test_total_cost_rejects_zero_boards():
    with pytest.raises(ValueError):
        BOM("test").total_cost(boards=0)


def test_exporter_writes_grouped_csv(tmp_path):
    bom = BOM("test")
    bom.add(resistor("R1"))
    bom.add(resistor("R2"))
    path = tmp_path / "bom.csv"

    BomExporter().to_csv(bom, path)

    rows = list(csv.reader(path.open(encoding="utf-8")))
    assert rows[0][0] == "Value"
    assert rows[1] == ["10k", "0805", "R1 R2", "2", "0.02", "0.04"]
    assert rows[-1] == ["TOTAL", "", "", "", "", "0.04"]
