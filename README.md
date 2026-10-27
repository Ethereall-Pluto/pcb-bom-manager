# PCB BOM Manager

A small Python tool for managing a Bill of Materials (BOM) for a printed circuit board:
add components by reference designator, merge identical parts into BOM lines,
calculate board cost for any batch size, and export the result to CSV.

Built as an object-oriented practice project, based on my background in electronics
and PCB design (Altium Designer, AutoCAD).

## Structure

| Class | Responsibility |
|---|---|
| `Component` | One part on the board (`R1`, `C3`, `U2`): value, footprint, unit price. Validates itself on creation. |
| `BOM` | The list of components for one board: add/remove, group identical parts, total cost. |
| `BomExporter` | Writes a BOM to CSV. Knows the file format, not the BOM rules. |

Design decisions:

- **Fail fast.** Duplicate designators, negative prices and conflicting prices for the same part raise an error immediately instead of producing a wrong BOM.
- **`Decimal` for money**, because `0.1 + 0.2 != 0.3` in floating point.
- **Immutable components** (`frozen=True`): a placed part changes by being replaced, not edited in place.
- **Export is separate from logic**, so adding JSON or XLSX export doesn't touch `BOM`.

## Usage

```bash
python demo.py
```

```
100n     0603    x1  C2
10k      0805    x2  R1 R2
10u      0805    x1  C1
330      0805    x1  R3
LED red  0805    x1  D1
NE555    SOIC-8  x1  U1
Cost per board: 0.60
Cost for 100 boards: 60.00
Saved bom.csv
```

## Tests

```bash
pip install pytest
pytest
```

Requires Python 3.10+.
