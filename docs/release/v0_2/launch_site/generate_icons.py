#!/usr/bin/env python3
"""Generate ObviousBench launch-site logo, favicon, and app-icon PNGs."""

from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "assets"
BASE = 512.0

INK = (23, 32, 29, 255)
RED = (218, 76, 58, 255)
PAPER = (244, 241, 232, 255)
TRANSPARENT = (0, 0, 0, 0)


def png_chunk(kind: bytes, data: bytes) -> bytes:
    checksum = zlib.crc32(kind + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", checksum)


def write_png(path: Path, width: int, height: int, rgba: bytes) -> None:
    raw = bytearray()
    stride = width * 4
    for y in range(height):
        raw.append(0)
        raw.extend(rgba[y * stride : (y + 1) * stride])
    payload = b"".join(
        [
            b"\x89PNG\r\n\x1a\n",
            png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)),
            png_chunk(b"IDAT", zlib.compress(bytes(raw), 9)),
            png_chunk(b"IEND", b""),
        ]
    )
    path.write_bytes(payload)


def line_distance(px: float, py: float, ax: float, ay: float, bx: float, by: float) -> float:
    vx = bx - ax
    vy = by - ay
    wx = px - ax
    wy = py - ay
    length_sq = vx * vx + vy * vy
    if length_sq == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, (wx * vx + wy * vy) / length_sq))
    qx = ax + t * vx
    qy = ay + t * vy
    return math.hypot(px - qx, py - qy)


def rounded_rect_sdf(
    px: float,
    py: float,
    x: float,
    y: float,
    width: float,
    height: float,
    radius: float,
) -> float:
    cx = x + width / 2.0
    cy = y + height / 2.0
    hx = width / 2.0 - radius
    hy = height / 2.0 - radius
    qx = abs(px - cx) - hx
    qy = abs(py - cy) - hy
    outside = math.hypot(max(qx, 0.0), max(qy, 0.0))
    inside = min(max(qx, qy), 0.0)
    return outside + inside - radius


def outline_sample(px: float, py: float) -> bool:
    distance = rounded_rect_sdf(px, py, 54.0, 76.0, 345.0, 336.0, 48.0)
    if abs(distance) > 16.0:
        return False
    return not (px > 333.0 and py < 232.0)


def check_sample(px: float, py: float) -> bool:
    stroke = 40.0
    return (
        line_distance(px, py, 137.0, 256.0, 216.0, 332.0) <= stroke / 2.0
        or line_distance(px, py, 216.0, 332.0, 452.0, 87.0) <= stroke / 2.0
        or math.hypot(px - 216.0, py - 332.0) <= stroke / 2.0
    )


def composite_over(
    dst: tuple[int, int, int, int],
    src: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    sr, sg, sb, sa = src
    dr, dg, db, da = dst
    if sa == 255:
        return src
    if sa == 0:
        return dst

    alpha = sa / 255.0
    dst_alpha = da / 255.0
    out_alpha = alpha + dst_alpha * (1.0 - alpha)
    if out_alpha == 0:
        return TRANSPARENT

    return (
        round((sr * alpha + dr * dst_alpha * (1.0 - alpha)) / out_alpha),
        round((sg * alpha + dg * dst_alpha * (1.0 - alpha)) / out_alpha),
        round((sb * alpha + db * dst_alpha * (1.0 - alpha)) / out_alpha),
        round(out_alpha * 255),
    )


def mark_sample(px: float, py: float, scale: float) -> tuple[int, int, int, int] | None:
    offset = (BASE - BASE * scale) / 2.0
    mx = (px - offset) / scale
    my = (py - offset) / scale
    if check_sample(mx, my):
        return RED
    if outline_sample(mx, my):
        return INK
    return None


def render(
    size: int,
    *,
    background: tuple[int, int, int, int],
    rounded_tile: bool = False,
    mark_scale: float = 1.0,
    supersample: int = 4,
) -> bytes:
    pixels = bytearray(size * size * 4)
    for y in range(size):
        for x in range(size):
            acc = [0, 0, 0, 0]
            for sy in range(supersample):
                for sx in range(supersample):
                    px = (x + (sx + 0.5) / supersample) * BASE / size
                    py = (y + (sy + 0.5) / supersample) * BASE / size

                    sample = background
                    if (
                        rounded_tile
                        and rounded_rect_sdf(px, py, 30.0, 30.0, 452.0, 452.0, 112.0) <= 0
                    ):
                        sample = composite_over(sample, PAPER)

                    mark_color = mark_sample(px, py, mark_scale)
                    if mark_color is not None:
                        sample = composite_over(sample, mark_color)

                    for index, channel in enumerate(sample):
                        acc[index] += channel

            samples = supersample * supersample
            offset = (y * size + x) * 4
            pixels[offset : offset + 4] = bytes(round(value / samples) for value in acc)
    return bytes(pixels)


def main() -> None:
    outputs = [
        ("obviousbench-mark.png", 512, TRANSPARENT, False, 1.0),
        ("favicon-16x16.png", 16, TRANSPARENT, False, 1.0),
        ("favicon-32x32.png", 32, TRANSPARENT, False, 1.0),
        ("apple-touch-icon.png", 180, TRANSPARENT, True, 0.74),
        ("icon-192.png", 192, TRANSPARENT, True, 0.74),
        ("icon-512.png", 512, TRANSPARENT, True, 0.74),
        ("icon-maskable-192.png", 192, PAPER, False, 0.70),
        ("icon-maskable-512.png", 512, PAPER, False, 0.70),
    ]
    for filename, size, background, rounded_tile, mark_scale in outputs:
        write_png(
            ROOT / filename,
            size,
            size,
            render(
                size,
                background=background,
                rounded_tile=rounded_tile,
                mark_scale=mark_scale,
            ),
        )


if __name__ == "__main__":
    main()
