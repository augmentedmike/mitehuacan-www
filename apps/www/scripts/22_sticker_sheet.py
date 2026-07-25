#!/usr/bin/env python3
"""Print sheets of "MAPA DE RUTAS" stickers from a full-sheet PSD layout.

The PSD (converted to PNG at 300 DPI) is the whole 13x19" sheet with
4 rows x 2 columns of pre-designed sticker artwork. Each sticker has an
80x80 px (at 75DPI native) white QR placeholder area that this script
fills with a unique tracking QR encoding https://mitehuacan.mx/qr/<id>.

Outputs to resources/stickers/: print-ready PDFs, preview PNGs, and CSVs.

Usage:
  python3 apps/www/scripts/22_sticker_sheet.py
    --start 1           # sticker id to start with (TEH-{n:04d})
    --sheets 5          # how many physical sheets to produce
    --csv               # optional: only regenerate CSVs, skip images
"""
import argparse
import csv
from pathlib import Path

import numpy as np
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
ART = Path("/Users/michaeloneal/Downloads/mapa-de-rutas.png")
OUT = ROOT / "resources" / "stickers"
BASE_URL = "https://mitehuacan.mx/qr/"

DPI = 300
SHEET_W_IN, SHEET_H_IN = 13, 19
SHEET_W, SHEET_H = SHEET_W_IN * DPI, SHEET_H_IN * DPI  # 3900 x 5700

# 8 sticker positions on the sheet — QR placeholder coordinates in px @ 300 DPI.
# Mapped from 75DPI native by ×4. Each placeholder is 320×320 px (80×80 at 75DPI).
QR_SLOTS = [
    # (x0, y0, x1, y1)
    (344,  468,  664,  788),    # Row 1, Left
    (2196, 468,  2516, 788),    # Row 1, Right
    (344,  1876, 664,  2196),   # Row 2, Left
    (2196, 1876, 2516, 2196),   # Row 2, Right
    (344,  3292, 664,  3612),   # Row 3, Left
    (2196, 3292, 2516, 3612),   # Row 3, Right
    (344,  4684, 664,  5004),   # Row 4, Left
    (2196, 4684, 2516, 5004),   # Row 4, Right
]

PER_SHEET = len(QR_SLOTS)
QR_FILL = 0.84
QR_RADIUS = 37


def make_qr(url):
    q = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=2)
    q.add_data(url)
    q.make(fit=True)
    img = np.array(q.make_image(fill_color="black", back_color="white").convert("RGBA"))
    white = (img[:, :, 0] > 200) & (img[:, :, 1] > 200) & (img[:, :, 2] > 200)
    img[white, 3] = 0
    return Image.fromarray(img, "RGBA")


def composite_qr_on_sheet(sheet, slot_idx, sticker_id):
    """Erase the white placeholder in the given slot and paste the QR."""
    x0, y0, x1, y1 = QR_SLOTS[slot_idx]
    draw = ImageDraw.Draw(sheet)
    draw.rounded_rectangle((x0, y0, x1, y1), radius=QR_RADIUS, fill=(255, 255, 255))
    box_w, box_h = x1 - x0, y1 - y0
    side = int(min(box_w, box_h) * QR_FILL)
    qr = make_qr(BASE_URL + sticker_id).resize((side, side), Image.NEAREST)
    px = x0 + (box_w - side) // 2
    py = y0 + (box_h - side) // 2
    sheet.paste(qr, (px, py), qr)


def main():
    ap = argparse.ArgumentParser(description="Generate sticker sheets from full-sheet PSD layout")
    ap.add_argument("--start", type=int, default=1, help="first sticker number (TEH-NNNN)")
    ap.add_argument("--sheets", type=int, default=1, help="number of physical sheets to produce")
    ap.add_argument("--count", type=int, help="total stickers to produce (overrides --sheets)")
    ap.add_argument("--csv", action="store_true", help="only regenerate CSVs, skip image processing")
    args = ap.parse_args()

    if not ART.exists():
        raise SystemExit(f"artwork not found: {ART}")
    OUT.mkdir(parents=True, exist_ok=True)

    if not args.csv:
        template = Image.open(ART).convert("RGB")
        if template.size != (SHEET_W, SHEET_H):
            template = template.resize((SHEET_W, SHEET_H), Image.LANCZOS)
            print(f"template resized to {template.size}")

    if args.count:
        num_sheets = (args.count + PER_SHEET - 1) // PER_SHEET
    else:
        num_sheets = args.sheets
    total_needed = args.count or (num_sheets * PER_SHEET)

    print(f"13x19in @ {DPI}dpi = {SHEET_W}x{SHEET_H}px; {PER_SHEET} stickers/sheet")
    n = args.start
    for s in range(num_sheets):
        if not args.csv:
            sheet = template.copy()
        rows_csv = []

        for slot_idx in range(PER_SHEET):
            if n > total_needed + args.start - 1:
                break
            sid = f"TEH-{n:04d}"
            if not args.csv:
                composite_qr_on_sheet(sheet, slot_idx, sid)
            rows_csv.append((sid, BASE_URL + sid))
            n += 1

        if not rows_csv:
            break

        idx = args.start // PER_SHEET + s + 1
        stem = f"mapa-de-rutas-sheet-{idx:02d}"

        if not args.csv:
            pdf = OUT / f"{stem}.pdf"
            sheet.save(pdf, "PDF", resolution=DPI)
            preview = OUT / f"{stem}-preview.png"
            sheet.resize((SHEET_W // 4, SHEET_H // 4), Image.LANCZOS).save(preview)

        csv_path = OUT / f"{stem}-ids.csv"
        with open(csv_path, "w", newline="") as f:
            csv.writer(f).writerows([("id", "url"), *rows_csv])

        count = len(rows_csv)
        ids_range = f"{rows_csv[0][0]}–{rows_csv[-1][0]}"
        if not args.csv:
            print(f"  {stem}: {count} stickers ({ids_range}) -> {pdf.name}, {preview.name}, ids.csv")
        else:
            print(f"  {stem}: {count} stickers ({ids_range}) -> ids.csv (csv-only)")


if __name__ == "__main__":
    main()
