import csv
from pathlib import Path

from bom.bom import BOM

HEADER = ["Value", "Footprint", "Designators", "Quantity", "Unit price", "Line cost"]


class BomExporter:
    """Writes a BOM to disk. Knows about file formats, nothing about BOM rules."""

    def to_csv(self, bom: BOM, path: Path) -> None:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADER)
            for line in bom.grouped():
                writer.writerow([
                    line.value,
                    line.footprint,
                    " ".join(line.designators),
                    line.quantity,
                    line.unit_price,
                    line.line_cost,
                ])
            writer.writerow(["TOTAL", "", "", "", "", bom.total_cost()])
