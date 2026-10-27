from decimal import Decimal
from pathlib import Path

from bom import BOM, BomExporter, Component


def main() -> None:
    bom = BOM("555 LED blinker")
    bom.add(Component("U1", "NE555", "SOIC-8", Decimal("0.40")))
    bom.add(Component("R1", "10k", "0805", Decimal("0.02")))
    bom.add(Component("R2", "10k", "0805", Decimal("0.02")))
    bom.add(Component("R3", "330", "0805", Decimal("0.02")))
    bom.add(Component("C1", "10u", "0805", Decimal("0.05")))
    bom.add(Component("C2", "100n", "0603", Decimal("0.03")))
    bom.add(Component("D1", "LED red", "0805", Decimal("0.06")))

    for line in bom.grouped():
        print(f"{line.value:<8} {line.footprint:<7} x{line.quantity}  {' '.join(line.designators)}")
    print(f"Cost per board: {bom.total_cost()}")
    print(f"Cost for 100 boards: {bom.total_cost(boards=100)}")

    output = Path("bom.csv")
    BomExporter().to_csv(bom, output)
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
