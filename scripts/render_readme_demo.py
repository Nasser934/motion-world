#!/usr/bin/env python3
"""Render the repository README demo without external assets."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import argparse
import math
import os
import subprocess

W, H = 1280, 720
FPS = 30
DURATION = 6


def lerp(a, b, t):
    return a + (b - a) * t


def ease(t):
    return t * t * (3 - 2 * t)


def clamp(value):
    return max(0, min(1, value))


def mix(a, b, t):
    return tuple(int(lerp(a[i], b[i], t)) for i in range(3))


def font_path(bold=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    return next((p for p in candidates if os.path.exists(p)), None)


def draw_leaf(draw, cx, cy, size, angle, fill):
    points = []
    for i in range(16):
        theta = 2 * math.pi * i / 16
        x = math.cos(theta) * size
        y = math.sin(theta) * size * 0.48
        ca, sa = math.cos(angle), math.sin(angle)
        points.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    draw.polygon(points, fill=fill)


def centered(draw, center, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text((center[0] - (box[2] - box[0]) / 2, center[1] - (box[3] - box[1]) / 2), text, font=font, fill=fill)


def render_frames(frames_dir: Path):
    frames_dir.mkdir(parents=True, exist_ok=True)
    regular = font_path(False)
    bold = font_path(True)
    f12 = ImageFont.truetype(regular, 12)
    f16 = ImageFont.truetype(regular, 16)
    f18 = ImageFont.truetype(regular, 18)
    f22 = ImageFont.truetype(bold, 22)
    f42 = ImageFont.truetype(bold, 42)

    count = FPS * DURATION
    for index in range(count):
        progress = index / (count - 1)
        p = ease(progress)
        image = Image.new("RGB", (W, H))
        pixels = image.load()
        top = mix((8, 12, 28), (24, 18, 60), p)
        bottom = mix((22, 31, 60), (15, 58, 78), p)
        for y in range(H):
            color = mix(top, bottom, y / (H - 1))
            for x in range(W):
                pixels[x, y] = color

        image = image.convert("RGBA")
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow, "RGBA")
        gx, gy = lerp(300, 980, p), lerp(250, 160, p)
        for radius, alpha in ((240, 22), (170, 28), (95, 45)):
            gd.ellipse((gx - radius, gy - radius, gx + radius, gy + radius), fill=(124, 92, 255, alpha))
        image = Image.alpha_composite(image, glow.filter(ImageFilter.GaussianBlur(35)))
        draw = ImageDraw.Draw(image)

        for i in range(28):
            sx = (i * 193) % W
            sy = 60 + ((i * 83) % 290)
            twinkle = (math.sin(index * 0.08 + i) + 1) / 2
            alpha = int(70 + 150 * twinkle * (1 - p * 0.35))
            radius = 2 if i % 3 == 0 else 1
            draw.ellipse((sx - radius, sy - radius, sx + radius, sy + radius), fill=(255, 255, 255, alpha))

        draw.text((70, 52), "MOTION WORLD", font=f22, fill=(186, 166, 255, 255))
        draw.text((70, 84), "One motion. Any driver. Any app.", font=f42, fill=(255, 255, 255, 255))
        draw.text((72, 142), "Images → video provider → motion package → native runtime", font=f18, fill=(202, 211, 235, 255))

        drivers = ["TIME", "SCROLL", "COUNT", "DRAG", "SENSOR", "STATE"]
        active = min(len(drivers) - 1, int(progress * len(drivers)))
        x = 72
        for driver_index, label in enumerate(drivers):
            width = 84 if label == "SENSOR" else 74
            is_active = driver_index == active
            fill = (114, 82, 230, 255) if is_active else (27, 35, 67, 255)
            outline = (180, 160, 255, 255) if is_active else (72, 84, 122, 255)
            draw.rounded_rectangle((x, 185, x + width, 218), radius=16, fill=fill, outline=outline, width=1)
            centered(draw, (x + width / 2, 201), label, f12, (255, 255, 255, 255 if is_active else 205))
            x += width + 10

        card = (64, 252, 892, 650)
        draw.rounded_rectangle(card, radius=34, fill=(10, 15, 36, 255), outline=(70, 80, 112, 255), width=1)
        stage = (94, 282, 862, 620)
        draw.rounded_rectangle(stage, radius=26, fill=(15, 26, 55, 255))

        sun_x, sun_y = lerp(190, 720, p), lerp(470, 330, p)
        sun_radius = 32 + 28 * p
        draw.ellipse((sun_x - sun_radius, sun_y - sun_radius, sun_x + sun_radius, sun_y + sun_radius), fill=(255, 197, 108, 255))

        island_y = 518 - 18 * math.sin(p * math.pi)
        draw.ellipse((245, 520, 715, 604), fill=(0, 0, 0, 110))
        draw.ellipse((225, island_y - 55, 735, island_y + 40), fill=(65, 96, 109, 255))
        draw.polygon([(250, island_y), (710, island_y), (640, island_y + 135), (320, island_y + 135)], fill=(34, 51, 66, 255))
        draw.ellipse((260, island_y - 50, 700, island_y + 23), fill=(69, 138, 112, 255))

        path_width = lerp(0, 170, clamp((progress - 0.12) / 0.35))
        draw.polygon([(450, island_y - 33), (510, island_y - 33), (510 + path_width * 0.52, island_y + 14), (450 - path_width * 0.15, island_y + 14)], fill=(219, 198, 147, 255))

        growth_x, ground = 480, island_y - 45
        seed_alpha = clamp(1 - progress / 0.18)
        if seed_alpha > 0:
            draw.ellipse((growth_x - 9, ground - 5, growth_x + 9, ground + 5), fill=(113, 76, 50, int(255 * seed_alpha)))

        growth = clamp((progress - 0.08) / 0.52)
        stem_height = 170 * ease(growth)
        draw.line((growth_x, ground, growth_x, ground - stem_height), fill=(85, 191, 123, 255), width=max(3, int(8 * growth)))
        if growth > 0.2:
            leaf_progress = clamp((growth - 0.2) / 0.8)
            leaf_specs = [(45, -0.45, 1), (72, 3.6, -1), (105, -0.52, 1), (132, 3.65, -1)]
            for leaf_index, (dy, angle, side) in enumerate(leaf_specs):
                lp = clamp((leaf_progress - leaf_index * 0.12) / 0.45)
                if lp > 0:
                    draw_leaf(draw, growth_x + side * 32 * lp, ground - dy * growth, 30 * lp, angle, (82, 205, 132, 255))

        canopy = clamp((progress - 0.42) / 0.35)
        if canopy > 0:
            for ox, oy, radius in [(-42, -160, 52), (0, -178, 66), (48, -158, 55), (-4, -135, 63)]:
                r = radius * ease(canopy)
                draw.ellipse((growth_x + ox - r, ground + oy - r, growth_x + ox + r, ground + oy + r), fill=(50, 181, 120, 255))

        house_progress = clamp((progress - 0.50) / 0.28)
        if house_progress > 0:
            hx, hy = 620, ground
            width = 130 * ease(house_progress)
            height = 96 * ease(house_progress)
            draw.rectangle((hx - width / 2, hy - height, hx + width / 2, hy), fill=(237, 224, 193, 255))
            draw.polygon([(hx - width * 0.62, hy - height), (hx, hy - height - 52 * house_progress), (hx + width * 0.62, hy - height)], fill=(137, 90, 94, 255))
            draw.rectangle((hx - 18, hy - 42 * house_progress, hx + 18, hy), fill=(103, 76, 71, 255))
            draw.rectangle((hx - 48, hy - 70 * house_progress, hx - 22, hy - 43 * house_progress), fill=(132, 191, 201, 255))

        for ripple_index in range(3):
            ripple_progress = clamp((progress - 0.30 - ripple_index * 0.08) / 0.45)
            if ripple_progress > 0:
                phase = (index / FPS * 0.25 + ripple_index * 0.25) % 1
                radius = 70 + 70 * phase
                alpha = int(90 * (1 - phase) * ripple_progress)
                draw.ellipse((480 - radius, island_y - 25 - radius * 0.16, 480 + radius, island_y - 25 + radius * 0.16), outline=(165, 229, 237, alpha), width=3)

        draw.text((116, 590), "NORMALIZED PROGRESS", font=f12, fill=(172, 189, 220, 255))
        draw.rounded_rectangle((300, 590, 765, 608), radius=9, fill=(39, 48, 79, 255))
        draw.rounded_rectangle((300, 590, 300 + 465 * p, 608), radius=9, fill=(120, 91, 246, 255))
        draw.text((780, 584), f"{int(progress * 100):02d}%", font=f22, fill=(255, 255, 255, 255))

        panel = (930, 252, 1215, 650)
        draw.rounded_rectangle(panel, radius=30, fill=(10, 15, 36, 255), outline=(70, 80, 112, 255), width=1)
        draw.text((965, 287), "RUNTIME PACKAGE", font=f16, fill=(186, 166, 255, 255))
        outputs = [("SCRUB MP4", "Fast seeking"), ("FRAMES", "Random access"), ("ATLAS", "Compact loops"), ("POSTERS", "Reduced motion")]
        y = 330
        revealed = 1 + int(progress * 3.99)
        for output_index, (title, subtitle) in enumerate(outputs):
            visible = output_index < revealed
            fill = (25, 33, 64, 255) if visible else (17, 23, 47, 255)
            outline = (61, 79, 107, 255) if visible else (39, 48, 73, 255)
            draw.rounded_rectangle((958, y, 1188, y + 58), radius=16, fill=fill, outline=outline, width=1)
            dot = (126, 234, 181, 255) if visible else (65, 76, 101, 255)
            draw.ellipse((974, y + 18, 990, y + 34), fill=dot)
            draw.text((1004, y + 10), title, font=f16, fill=(255, 255, 255, 255 if visible else 110))
            draw.text((1004, y + 32), subtitle, font=f12, fill=(185, 198, 225, 255 if visible else 105))
            y += 70
        draw.text((965, 619), "SwiftUI  •  Compose  •  Flutter", font=f12, fill=(178, 191, 220, 255))
        draw.text((70, 684), "Provider-agnostic • Offline runtime • Deterministic 0…1 control", font=f12, fill=(165, 178, 205, 255))

        image.convert("RGB").save(frames_dir / f"frame_{index:04d}.png", quality=95)


def encode(root: Path, frames_dir: Path):
    mp4 = root / "motion-world-demo.mp4"
    gif = root / "motion-world-demo.gif"
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS), "-i", str(frames_dir / "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-movflags", "+faststart", str(mp4)
    ], check=True)
    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y", "-i", str(mp4),
        "-vf", "fps=12,scale=800:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=96[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5",
        "-loop", "0", str(gif)
    ], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="docs/media")
    args = parser.parse_args()
    root = Path(args.out).resolve()
    frames = root / "demo-frames"
    render_frames(frames)
    encode(root, frames)
    print(f"Created {root / 'motion-world-demo.mp4'}")
    print(f"Created {root / 'motion-world-demo.gif'}")


if __name__ == "__main__":
    main()
