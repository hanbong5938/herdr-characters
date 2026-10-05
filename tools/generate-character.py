#!/usr/bin/env python3
"""Generate OMPet's original, transparent character artwork.

This module intentionally uses only Python's standard library.  Shapes are
rasterized at four times the final resolution and box-filtered down to keep
small details clean without requiring Pillow or another image dependency.
"""

from __future__ import annotations

import argparse
import json
import math
import struct
import zlib
from pathlib import Path
from typing import Iterable, Sequence

WIDTH = 384
HEIGHT = 512
SUPERSAMPLE = 4
SW = WIDTH * SUPERSAMPLE
SH = HEIGHT * SUPERSAMPLE

# A compact, deliberately original palette: lavender shell, teal circuitry,
# and warm face accents against a deep indigo outline.
INK = (42, 37, 77, 255)
INK_SOFT = (64, 54, 105, 255)
LAVENDER = (171, 145, 231, 255)
LAVENDER_LIGHT = (213, 198, 255, 255)
LAVENDER_HIGHLIGHT = (235, 227, 255, 255)
LAVENDER_DARK = (119, 86, 183, 255)
TEAL = (67, 202, 195, 255)
TEAL_DARK = (30, 124, 143, 255)
MINT = (150, 241, 218, 255)
CREAM = (255, 248, 238, 255)
PINK = (255, 142, 192, 255)
PINK_LIGHT = (255, 187, 215, 255)
GOLD = (255, 205, 104, 255)
WHITE = (255, 255, 255, 255)
TRANSPARENT = (0, 0, 0, 0)


Color = tuple[int, int, int, int]
Point = tuple[float, float]


def _clamp(value: int, low: int = 0, high: int = 255) -> int:
    return max(low, min(high, value))


def _scaled(value: float) -> int:
    return int(round(value * SUPERSAMPLE))


class Canvas:
    """A tiny RGBA raster canvas with alpha compositing and vector helpers."""

    def __init__(self, width: int = WIDTH, height: int = HEIGHT) -> None:
        self.width = width
        self.height = height
        self.sw = width * SUPERSAMPLE
        self.sh = height * SUPERSAMPLE
        self.pixels = bytearray(self.sw * self.sh * 4)

    def _blend(self, x: int, y: int, color: Color) -> None:
        if x < 0 or y < 0 or x >= self.sw or y >= self.sh:
            return
        sr, sg, sb, sa = color
        if sa <= 0:
            return
        index = (y * self.sw + x) * 4
        if sa >= 255:
            self.pixels[index : index + 4] = bytes((sr, sg, sb, 255))
            return
        dr, dg, db, da = self.pixels[index : index + 4]
        inverse = 255 - sa
        out_a = sa + (da * inverse + 127) // 255
        if out_a <= 0:
            return
        self.pixels[index] = _clamp((sr * sa + dr * da * inverse // 255) // out_a)
        self.pixels[index + 1] = _clamp(
            (sg * sa + dg * da * inverse // 255) // out_a
        )
        self.pixels[index + 2] = _clamp(
            (sb * sa + db * da * inverse // 255) // out_a
        )
        self.pixels[index + 3] = _clamp(out_a)

    def _span(self, y: int, start: int, end: int, color: Color) -> None:
        if y < 0 or y >= self.sh:
            return
        start = max(0, start)
        end = min(self.sw - 1, end)
        if start > end:
            return
        for x in range(start, end + 1):
            self._blend(x, y, color)

    def polygon(self, points: Sequence[Point], color: Color) -> None:
        if len(points) < 3:
            return
        scaled = [(_scaled(x), _scaled(y)) for x, y in points]
        min_y = max(0, min(y for _, y in scaled))
        max_y = min(self.sh - 1, max(y for _, y in scaled))
        count = len(scaled)
        for y in range(min_y, max_y + 1):
            intersections: list[float] = []
            for index, (x0, y0) in enumerate(scaled):
                x1, y1 = scaled[(index + 1) % count]
                if y0 == y1:
                    continue
                # Half-open scanline convention avoids double filling vertices.
                if (y0 <= y < y1) or (y1 <= y < y0):
                    intersections.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            intersections.sort()
            for index in range(0, len(intersections) - 1, 2):
                start = math.ceil(intersections[index])
                end = math.floor(intersections[index + 1])
                self._span(y, start, end, color)

    def ellipse(self, box: tuple[float, float, float, float], color: Color) -> None:
        left, top, right, bottom = (_scaled(value) for value in box)
        if right <= left or bottom <= top:
            return
        center_x = (left + right) / 2.0
        center_y = (top + bottom) / 2.0
        radius_x = (right - left) / 2.0
        radius_y = (bottom - top) / 2.0
        for y in range(max(0, top), min(self.sh - 1, bottom) + 1):
            normalized_y = (y + 0.5 - center_y) / radius_y
            if abs(normalized_y) > 1:
                continue
            half_width = radius_x * math.sqrt(max(0.0, 1.0 - normalized_y**2))
            self._span(y, math.ceil(center_x - half_width), math.floor(center_x + half_width), color)

    def stroke(
        self,
        points: Sequence[Point],
        color: Color,
        width: float,
        closed: bool = False,
    ) -> None:
        if len(points) < 2:
            return
        path = list(points)
        if closed:
            path.append(path[0])
        radius = width / 2.0
        for start, end in zip(path, path[1:]):
            x0, y0 = start
            x1, y1 = end
            dx = x1 - x0
            dy = y1 - y0
            length = math.hypot(dx, dy)
            if length < 1e-6:
                self.ellipse((x0 - radius, y0 - radius, x0 + radius, y0 + radius), color)
                continue
            nx = -dy / length * radius
            ny = dx / length * radius
            self.polygon(
                ((x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)),
                color,
            )
            self.ellipse((x0 - radius, y0 - radius, x0 + radius, y0 + radius), color)
            self.ellipse((x1 - radius, y1 - radius, x1 + radius, y1 + radius), color)

    def downsample(self) -> bytes:
        """Box-filter the supersampled image into final-size RGBA bytes."""
        result = bytearray(self.width * self.height * 4)
        area = SUPERSAMPLE * SUPERSAMPLE
        output_index = 0
        for y in range(self.height):
            base_y = y * SUPERSAMPLE
            for x in range(self.width):
                base_x = x * SUPERSAMPLE
                sums = [0, 0, 0, 0]
                for sub_y in range(SUPERSAMPLE):
                    row = ((base_y + sub_y) * self.sw + base_x) * 4
                    for sub_x in range(SUPERSAMPLE):
                        index = row + sub_x * 4
                        sums[0] += self.pixels[index]
                        sums[1] += self.pixels[index + 1]
                        sums[2] += self.pixels[index + 2]
                        sums[3] += self.pixels[index + 3]
                result[output_index : output_index + 4] = bytes(
                    value // area for value in sums
                )
                output_index += 4
        return bytes(result)


def cubic(start: Point, control_a: Point, control_b: Point, end: Point, steps: int = 12) -> list[Point]:
    points: list[Point] = []
    for index in range(steps + 1):
        t = index / steps
        inverse = 1.0 - t
        points.append(
            (
                inverse**3 * start[0]
                + 3 * inverse**2 * t * control_a[0]
                + 3 * inverse * t**2 * control_b[0]
                + t**3 * end[0],
                inverse**3 * start[1]
                + 3 * inverse**2 * t * control_a[1]
                + 3 * inverse * t**2 * control_b[1]
                + t**3 * end[1],
            )
        )
    return points


def offset(points: Iterable[Point], dx: float, dy: float) -> list[Point]:
    return [(x + dx, y + dy) for x, y in points]


def rounded_rect(canvas: Canvas, box: tuple[float, float, float, float], radius: float, color: Color) -> None:
    left, top, right, bottom = box
    radius = min(radius, (right - left) / 2, (bottom - top) / 2)
    canvas.polygon(((left + radius, top), (right - radius, top), (right - radius, bottom), (left + radius, bottom)), color)
    canvas.polygon(((left, top + radius), (right, top + radius), (right, bottom - radius), (left, bottom - radius)), color)
    canvas.ellipse((left, top, left + radius * 2, top + radius * 2), color)
    canvas.ellipse((right - radius * 2, top, right, top + radius * 2), color)
    canvas.ellipse((left, bottom - radius * 2, left + radius * 2, bottom), color)
    canvas.ellipse((right - radius * 2, bottom - radius * 2, right, bottom), color)


def outlined_rounded_rect(
    canvas: Canvas,
    box: tuple[float, float, float, float],
    radius: float,
    fill: Color,
    outline: Color = INK,
    width: float = 6,
) -> None:
    rounded_rect(canvas, box, radius + width / 2, outline)
    inset = width
    rounded_rect(canvas, (box[0] + inset, box[1] + inset, box[2] - inset, box[3] - inset), max(0, radius - width / 2), fill)


def draw_paw(canvas: Canvas, center: Point, scale: float = 1.0, color: Color = LAVENDER_LIGHT) -> None:
    x, y = center
    canvas.ellipse((x - 15 * scale, y - 12 * scale, x + 15 * scale, y + 14 * scale), INK)
    canvas.ellipse((x - 11 * scale, y - 9 * scale, x + 11 * scale, y + 11 * scale), color)
    for toe_x in (-6, 0, 6):
        canvas.ellipse((x + (toe_x - 2.0) * scale, y + 5 * scale, x + (toe_x + 2.0) * scale, y + 10 * scale), INK_SOFT)


def draw_tail(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    if pose == "running":
        points = offset(cubic((112, 355), (64, 337), (52, 279), (80, 250), 18), dx, dy)
        points += offset(cubic((80, 250), (94, 232), (123, 240), (133, 255), 10)[1:], dx, dy)
    elif pose == "unknown":
        points = offset(cubic((115, 366), (69, 373), (60, 414), (91, 431), 16), dx, dy)
        points += offset(cubic((91, 431), (107, 443), (119, 430), (113, 416), 9)[1:], dx, dy)
    else:
        points = offset(cubic((116, 354), (63, 362), (54, 426), (96, 430), 18), dx, dy)
        points += offset(cubic((96, 430), (128, 433), (128, 396), (112, 390), 10)[1:], dx, dy)
    canvas.stroke(points, INK, 32, closed=False)
    canvas.stroke(points, TEAL, 23, closed=False)
    highlight = points[max(1, len(points) // 5) : max(2, len(points) // 2)]
    if len(highlight) > 1:
        canvas.stroke(highlight, MINT, 4, closed=False)


def draw_speed_marks(canvas: Canvas, dx: float, dy: float) -> None:
    marks = [
        ((45, 212), (80, 205), 6, TEAL),
        ((29, 235), (63, 229), 4, GOLD),
        ((48, 407), (82, 399), 5, PINK),
        ((288, 264), (328, 254), 5, MINT),
    ]
    for start, end, width, color in marks:
        canvas.stroke(offset((start, end), dx, dy), color, width)


def body_path(dx: float, dy: float) -> list[Point]:
    points = offset(cubic((113, 244), (93, 271), (93, 355), (112, 410), 16), dx, dy)
    points += offset(cubic((112, 410), (126, 446), (253, 446), (272, 409), 18)[1:], dx, dy)
    points += offset(cubic((272, 409), (291, 355), (287, 271), (268, 244), 16)[1:], dx, dy)
    points += offset(cubic((268, 244), (239, 223), (139, 223), (113, 244), 14)[1:], dx, dy)
    return points


def head_path(dx: float, dy: float) -> list[Point]:
    points = offset(cubic((99, 144), (95, 122), (103, 83), (112, 61), 11), dx, dy)
    points += offset(cubic((112, 61), (128, 65), (143, 75), (157, 87), 10)[1:], dx, dy)
    points += offset(cubic((157, 87), (170, 78), (181, 70), (192, 60), 9)[1:], dx, dy)
    points += offset(cubic((192, 60), (204, 69), (219, 79), (230, 87), 9)[1:], dx, dy)
    points += offset(cubic((230, 87), (246, 74), (261, 66), (273, 61), 10)[1:], dx, dy)
    points += offset(cubic((273, 61), (284, 84), (291, 122), (285, 151), 12)[1:], dx, dy)
    points += offset(cubic((285, 151), (283, 198), (252, 226), (193, 231), 17)[1:], dx, dy)
    points += offset(cubic((193, 231), (137, 228), (105, 202), (99, 144), 16)[1:], dx, dy)
    return points


def draw_back_legs(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    if pose == "running":
        legs = [((146, 386), (116, 435), (108, 447)), ((235, 386), (269, 415), (289, 415))]
    elif pose == "unknown":
        legs = [((148, 393), (143, 434), (139, 444)), ((229, 394), (239, 433), (248, 441))]
    else:
        legs = [((145, 390), (137, 432), (132, 443)), ((233, 390), (240, 432), (247, 443))]
    for points in legs:
        path = offset(points, dx, dy)
        canvas.stroke(path, INK, 25)
        canvas.stroke(path, LAVENDER_DARK, 16)
        draw_paw(canvas, (path[-1][0], path[-1][1] + 4), 0.93, LAVENDER_LIGHT)


def draw_back_arm(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    if pose == "running":
        path = offset(((266, 278), (304, 300), (319, 337)), dx, dy)
        canvas.stroke(path, INK, 27)
        canvas.stroke(path, LAVENDER_DARK, 17)
        draw_paw(canvas, (319 + dx, 340 + dy), 0.9, LAVENDER_LIGHT)
    elif pose == "waiting":
        path = offset(((108, 280), (80, 310), (76, 347)), dx, dy)
        canvas.stroke(path, INK, 27)
        canvas.stroke(path, LAVENDER_DARK, 17)
        draw_paw(canvas, (75 + dx, 350 + dy), 0.88, LAVENDER_LIGHT)
    elif pose == "unknown":
        path = offset(((108, 283), (79, 303), (77, 336)), dx, dy)
        canvas.stroke(path, INK, 27)
        canvas.stroke(path, LAVENDER_DARK, 17)
        draw_paw(canvas, (76 + dx, 339 + dy), 0.88, LAVENDER_LIGHT)
    else:
        path = offset(((109, 283), (83, 318), (81, 349)), dx, dy)
        canvas.stroke(path, INK, 27)
        canvas.stroke(path, LAVENDER_DARK, 17)
        draw_paw(canvas, (80 + dx, 352 + dy), 0.88, LAVENDER_LIGHT)


def draw_torso(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    torso = body_path(dx, dy)
    canvas.polygon(torso, INK)
    inner = offset(body_path(0, 0), dx, dy)
    # Inset by layering a slightly smaller, softer silhouette.
    inner = offset(cubic((119, 251), (105, 282), (105, 352), (121, 402), 15), dx, dy)
    inner += offset(cubic((121, 402), (139, 432), (239, 432), (263, 401), 16)[1:], dx, dy)
    inner += offset(cubic((263, 401), (279, 351), (276, 282), (261, 252), 15)[1:], dx, dy)
    inner += offset(cubic((261, 252), (231, 235), (146, 235), (119, 251), 13)[1:], dx, dy)
    canvas.polygon(inner, LAVENDER)

    # A light shell rim and a darker side panel give the body a manufactured form.
    rim = offset(cubic((123, 255), (111, 290), (113, 355), (127, 391), 14), dx, dy)
    canvas.stroke(rim, LAVENDER_LIGHT, 6)
    side = offset(cubic((252, 252), (274, 292), (271, 360), (254, 399), 14), dx, dy)
    canvas.stroke(side, LAVENDER_DARK, 8)

    outlined_rounded_rect(
        canvas,
        (137 + dx, 274 + dy, 249 + dx, 398 + dy),
        29,
        (128, 225, 218, 255),
        INK,
        7,
    )
    # Chest panel glow and horizontal vent marks.
    rounded_rect(canvas, (148 + dx, 288 + dy, 238 + dx, 384 + dy), 20, (99, 203, 201, 255))
    canvas.ellipse((157 + dx, 299 + dy, 229 + dx, 369 + dy), (87, 186, 190, 255))
    canvas.ellipse((166 + dx, 307 + dy, 220 + dx, 360 + dy), (112, 219, 207, 255))
    canvas.stroke(offset(((165, 322), (220, 322)), dx, dy), MINT, 5)
    canvas.stroke(offset(((162, 338), (224, 338)), dx, dy), TEAL_DARK, 4)
    canvas.stroke(offset(((168, 351), (216, 351)), dx, dy), MINT, 4)
    # Small central status diamond: a coding-familiar signature rather than text.
    canvas.polygon(offset(((193, 314), (205, 327), (193, 340), (181, 327)), dx, dy), INK)
    canvas.polygon(offset(((193, 319), (200, 327), (193, 335), (186, 327)), dx, dy), GOLD)

    if pose == "running":
        canvas.stroke(offset(((151, 373), (170, 381)), dx, dy), WHITE, 4)
        canvas.stroke(offset(((216, 381), (234, 373)), dx, dy), WHITE, 4)
    elif pose == "waiting":
        canvas.ellipse((177 + dx, 370 + dy, 185 + dx, 378 + dy), GOLD)
        canvas.ellipse((201 + dx, 370 + dy, 209 + dx, 378 + dy), GOLD)
    elif pose == "unknown":
        canvas.stroke(offset(((169, 371), (183, 377), (193, 370), (203, 377), (216, 371)), dx, dy), PINK_LIGHT, 4)


def draw_front_arm(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    if pose == "running":
        path = offset(((116, 281), (83, 259), (71, 229)), dx, dy)
        canvas.stroke(path, INK, 28)
        canvas.stroke(path, LAVENDER, 18)
        draw_paw(canvas, (69 + dx, 225 + dy), 0.92, LAVENDER_LIGHT)
        canvas.stroke(offset(((62, 220), (55, 215)), dx, dy), INK_SOFT, 3)
        canvas.stroke(offset(((67, 218), (63, 210)), dx, dy), INK_SOFT, 3)
    elif pose == "waiting":
        # Raised wave with three separated fingers.
        path = offset(((257, 284), (273, 249), (275, 203)), dx, dy)
        canvas.stroke(path, INK, 28)
        canvas.stroke(path, LAVENDER, 18)
        draw_paw(canvas, (276 + dx, 193 + dy), 1.02, LAVENDER_LIGHT)
        for x, lean in ((267, -4), (275, 0), (283, 4)):
            canvas.stroke(offset(((x, 187), (x + lean, 177)), dx, dy), INK_SOFT, 3)
    elif pose == "unknown":
        path = offset(((257, 292), (246, 302), (232, 316)), dx, dy)
        canvas.stroke(path, INK, 28)
        canvas.stroke(path, LAVENDER, 18)
        draw_paw(canvas, (226 + dx, 319 + dy), 0.94, LAVENDER_LIGHT)
        canvas.stroke(offset(((222, 315), (218, 306)), dx, dy), INK_SOFT, 3)
    else:
        path = offset(((260, 282), (291, 316), (296, 350)), dx, dy)
        canvas.stroke(path, INK, 27)
        canvas.stroke(path, LAVENDER, 17)
        draw_paw(canvas, (297 + dx, 353 + dy), 0.88, LAVENDER_LIGHT)


def draw_head(canvas: Canvas, pose: str, dx: float, dy: float) -> None:
    head = head_path(dx, dy)
    canvas.polygon(head, INK)
    inner = offset(cubic((106, 145), (104, 122), (109, 95), (116, 73), 11), dx, dy)
    inner += offset(cubic((116, 73), (132, 78), (145, 88), (158, 98), 10)[1:], dx, dy)
    inner += offset(cubic((158, 98), (171, 90), (182, 81), (192, 72), 9)[1:], dx, dy)
    inner += offset(cubic((192, 72), (205, 81), (218, 91), (230, 98), 9)[1:], dx, dy)
    inner += offset(cubic((230, 98), (246, 85), (258, 78), (269, 73), 10)[1:], dx, dy)
    inner += offset(cubic((269, 73), (278, 96), (282, 124), (278, 149), 11)[1:], dx, dy)
    inner += offset(cubic((278, 149), (276, 190), (248, 216), (193, 220), 16)[1:], dx, dy)
    inner += offset(cubic((193, 220), (142, 218), (112, 192), (106, 145), 15)[1:], dx, dy)
    canvas.polygon(inner, LAVENDER)

    # Ear insets, with a little teal circuitry at each base.
    canvas.polygon(offset(((115, 76), (151, 96), (119, 111)), dx, dy), LAVENDER_DARK)
    canvas.polygon(offset(((119, 83), (142, 96), (122, 101)), dx, dy), PINK_LIGHT)
    canvas.polygon(offset(((268, 77), (232, 97), (265, 111)), dx, dy), LAVENDER_DARK)
    canvas.polygon(offset(((264, 84), (241, 96), (261, 101)), dx, dy), PINK_LIGHT)
    canvas.stroke(offset(((129, 104), (136, 111), (145, 107)), dx, dy), TEAL, 4)
    canvas.stroke(offset(((257, 104), (250, 111), (241, 107)), dx, dy), TEAL, 4)

    # Brow plates and cheeks keep the face readable at small size.
    canvas.stroke(offset(((128, 132), (158, 124)), dx, dy), LAVENDER_LIGHT, 7)
    canvas.stroke(offset(((228, 124), (258, 132)), dx, dy), LAVENDER_LIGHT, 7)
    canvas.ellipse((116 + dx, 170 + dy, 143 + dx, 185 + dy), PINK_LIGHT)
    canvas.ellipse((242 + dx, 170 + dy, 269 + dx, 185 + dy), PINK_LIGHT)

    if pose == "running":
        draw_eye(canvas, (151 + dx, 151 + dy), "focused")
        draw_eye(canvas, (235 + dx, 151 + dy), "focused")
        canvas.polygon(offset(((190, 169), (196, 169), (193, 175)), dx, dy), TEAL_DARK)
        canvas.stroke(offset(cubic((179, 181), (187, 191), (201, 191), (210, 181), 10), dx, dy), INK, 5)
        canvas.ellipse((188 + dx, 183 + dy, 202 + dx, 193 + dy), PINK)
    elif pose == "waiting":
        draw_eye(canvas, (151 + dx, 151 + dy), "bright")
        canvas.stroke(offset(((226, 155), (235, 160), (244, 155)), dx, dy), INK, 5)
        canvas.polygon(offset(((190, 169), (196, 169), (193, 175)), dx, dy), TEAL_DARK)
        canvas.stroke(offset(cubic((178, 183), (188, 190), (199, 190), (209, 181), 10), dx, dy), INK, 5)
    elif pose == "unknown":
        draw_eye(canvas, (150 + dx, 150 + dy), "wide")
        draw_eye(canvas, (237 + dx, 153 + dy), "uneven")
        canvas.polygon(offset(((190, 169), (196, 169), (193, 176)), dx, dy), TEAL_DARK)
        canvas.stroke(offset(cubic((180, 190), (188, 182), (199, 182), (207, 190), 10), dx, dy), INK, 5)
    else:
        draw_eye(canvas, (151 + dx, 151 + dy), "soft")
        draw_eye(canvas, (235 + dx, 151 + dy), "soft")
        canvas.polygon(offset(((190, 169), (196, 169), (193, 175)), dx, dy), TEAL_DARK)
        canvas.stroke(offset(cubic((179, 181), (187, 192), (200, 192), (209, 181), 10), dx, dy), INK, 5)

    # A tiny forehead indicator changes color with the current mode.
    indicator = {"idle": MINT, "running": GOLD, "waiting": TEAL, "unknown": PINK}[pose]
    canvas.ellipse((187 + dx, 105 + dy, 199 + dx, 117 + dy), INK)
    canvas.ellipse((190 + dx, 108 + dy, 196 + dx, 114 + dy), indicator)


def draw_eye(canvas: Canvas, center: Point, mode: str) -> None:
    x, y = center
    if mode == "soft":
        canvas.ellipse((x - 17, y - 14, x + 17, y + 17), INK)
        canvas.ellipse((x - 12, y - 10, x + 12, y + 12), CREAM)
        canvas.ellipse((x - 5, y - 7, x + 7, y + 9), TEAL_DARK)
        canvas.ellipse((x - 3, y - 6, x + 1, y - 2), WHITE)
    elif mode == "focused":
        canvas.ellipse((x - 18, y - 10, x + 18, y + 12), INK)
        canvas.ellipse((x - 13, y - 7, x + 13, y + 8), CREAM)
        canvas.ellipse((x - 5, y - 6, x + 8, y + 8), TEAL_DARK)
        canvas.ellipse((x - 3, y - 5, x + 1, y - 1), WHITE)
    elif mode == "bright":
        canvas.ellipse((x - 17, y - 17, x + 17, y + 18), INK)
        canvas.ellipse((x - 12, y - 13, x + 12, y + 13), CREAM)
        canvas.ellipse((x - 5, y - 9, x + 8, y + 9), TEAL_DARK)
        canvas.ellipse((x - 3, y - 8, x + 1, y - 4), WHITE)
    elif mode == "wide":
        canvas.ellipse((x - 18, y - 19, x + 18, y + 19), INK)
        canvas.ellipse((x - 13, y - 15, x + 13, y + 14), CREAM)
        canvas.ellipse((x - 5, y - 10, x + 8, y + 10), TEAL_DARK)
        canvas.ellipse((x - 3, y - 9, x + 2, y - 4), WHITE)
    else:  # uneven worried eye
        canvas.ellipse((x - 15, y - 13, x + 16, y + 16), INK)
        canvas.ellipse((x - 11, y - 9, x + 11, y + 11), CREAM)
        canvas.ellipse((x - 4, y - 7, x + 7, y + 8), TEAL_DARK)
        canvas.ellipse((x - 2, y - 6, x + 2, y - 2), WHITE)


def draw_idle_accents(canvas: Canvas, dx: float, dy: float) -> None:
    # Three small circuit-like sparkles reinforce that this is a coding familiar.
    canvas.stroke(offset(((54, 133), (62, 133), (66, 126), (74, 126)), dx, dy), TEAL, 4)
    canvas.ellipse((52 + dx, 130 + dy, 59 + dx, 137 + dy), GOLD)
    canvas.stroke(offset(((316, 377), (327, 377), (333, 369)), dx, dy), PINK, 4)
    canvas.ellipse((326 + dx, 367 + dy, 334 + dx, 375 + dy), MINT)
    canvas.polygon(offset(((307, 88), (312, 98), (322, 102), (312, 106), (307, 117), (303, 106), (293, 102), (303, 98)), dx, dy), GOLD)


def draw_waiting_accents(canvas: Canvas, dx: float, dy: float) -> None:
    # A patient ellipsis bubble, clearly separate from the character silhouette.
    outlined_rounded_rect(canvas, (286 + dx, 104 + dy, 350 + dx, 145 + dy), 15, CREAM, INK, 5)
    canvas.polygon(offset(((296, 142), (307, 142), (300, 153)), dx, dy), INK)
    for x in (303, 318, 333):
        canvas.ellipse((x - 4 + dx, 120 + dy, x + 4 + dx, 128 + dy), TEAL_DARK)
    canvas.ellipse((48 + dx, 105 + dy, 58 + dx, 115 + dy), GOLD)
    canvas.stroke(offset(((53, 100), (53, 91)), dx, dy), GOLD, 3)


def draw_unknown_accents(canvas: Canvas, dx: float, dy: float) -> None:
    # The question badge uses hand-drawn geometry, so no font or platform asset is needed.
    outlined_rounded_rect(canvas, (286 + dx, 79 + dy, 345 + dx, 140 + dy), 19, LAVENDER_HIGHLIGHT, INK, 6)
    canvas.polygon(offset(((298, 137), (311, 137), (304, 151)), dx, dy), INK)
    canvas.stroke(offset(cubic((305, 99), (311, 88), (328, 91), (328, 102), 9), dx, dy), TEAL_DARK, 6)
    canvas.stroke(offset(((328, 102), (317, 113), (317, 119)), dx, dy), TEAL_DARK, 6)
    canvas.ellipse((314 + dx, 127 + dy, 321 + dx, 134 + dy), TEAL_DARK)
    canvas.stroke(offset(((50, 112), (64, 112)), dx, dy), PINK, 4)
    canvas.stroke(offset(((57, 105), (57, 119)), dx, dy), PINK, 4)


def draw_character(pose: str) -> Canvas:
    canvas = Canvas()
    offsets = {
        "idle": (0.0, 0.0),
        "running": (5.0, -8.0),
        "waiting": (0.0, 0.0),
        "unknown": (0.0, 7.0),
    }
    dx, dy = offsets[pose]

    # A soft contact shadow anchors each transparent sprite without a backdrop.
    shadow_y = {"idle": 456, "running": 451, "waiting": 456, "unknown": 463}[pose]
    canvas.ellipse((68 + dx, shadow_y - 10 + dy, 316 + dx, shadow_y + 18 + dy), (39, 35, 71, 72))
    draw_tail(canvas, pose, dx, dy)
    if pose == "running":
        draw_speed_marks(canvas, dx, dy)
    draw_back_legs(canvas, pose, dx, dy)
    draw_back_arm(canvas, pose, dx, dy)
    draw_torso(canvas, pose, dx, dy)
    draw_front_arm(canvas, pose, dx, dy)
    draw_head(canvas, pose, dx, dy)

    if pose == "idle":
        draw_idle_accents(canvas, dx, dy)
    elif pose == "waiting":
        draw_waiting_accents(canvas, dx, dy)
    elif pose == "unknown":
        draw_unknown_accents(canvas, dx, dy)
    else:
        # Running has a small teal trail under the feet instead of a speech badge.
        canvas.stroke(offset(((93, 451), (122, 451)), dx, dy), TEAL, 4)
        canvas.stroke(offset(((274, 441), (307, 435)), dx, dy), GOLD, 4)
    return canvas


def _png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def write_png(path: Path, rgba: bytes, width: int = WIDTH, height: int = HEIGHT) -> None:
    rows = bytearray()
    stride = width * 4
    for row in range(height):
        rows.append(0)  # PNG filter type: None, deterministic and easy to inspect.
        start = row * stride
        rows.extend(rgba[start : start + stride])
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png.extend(_png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)))
    png.extend(_png_chunk(b"IDAT", zlib.compress(bytes(rows), level=9)))
    png.extend(_png_chunk(b"IEND", b""))
    path.write_bytes(png)


def generate(output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for pose in ("idle", "running", "waiting", "unknown"):
        image = draw_character(pose).downsample()
        write_png(output / f"{pose}.png", image)
    manifest = {
        "version": 1,
        "name": "OMPet",
        "width": WIDTH,
        "height": HEIGHT,
        "poses": {
            "idle": "idle.png",
            "running": "running.png",
            "waiting": "waiting.png",
            "unknown": "unknown.png",
        },
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2, separators=(",", ": ")) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate OMPet's original character assets")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "sources" / "legacy-png",
        help="directory receiving manifest.json and the four transparent PNG poses",
    )
    args = parser.parse_args()
    generate(args.output.resolve())


if __name__ == "__main__":
    main()
