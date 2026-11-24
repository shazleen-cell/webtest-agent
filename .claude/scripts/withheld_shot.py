#!/usr/bin/env python3
"""Make the "evidence withheld" image for a step that must not be captured (the card step of a payment-invalid run).

Usage: withheld_shot.py <RUN> <TC ID> <step number> [<step number> ...]
Writes RUN/<TC ID>/stepNN.png (1440x900) saying the screenshot was withheld on purpose, so the replay, the steps PDF and the
report have an image for the step without ever capturing the card form."""
import os, sys
from PIL import Image, ImageDraw

if len(sys.argv) < 4:
    sys.exit(__doc__)
run, tc = os.path.abspath(sys.argv[1]), sys.argv[2]
os.makedirs(os.path.join(run, tc), exist_ok=True)
for n in sys.argv[3:]:
    img = Image.new("RGB", (1440, 900), (236, 238, 243))
    d = ImageDraw.Draw(img)
    d.rectangle([40, 40, 1400, 860], outline=(150, 156, 170), width=4)
    d.text((620, 410), "EVIDENCE WITHHELD", fill=(60, 66, 80))
    d.text((520, 440), "Card step: nothing is captured while the card form is filled.", fill=(60, 66, 80))
    d.text((620, 470), f"{tc} step {int(n)}", fill=(60, 66, 80))
    path = os.path.join(run, tc, f"step{int(n):02d}.png")
    img.save(path)
    print(path)
