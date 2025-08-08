from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap, uuid, os

def center_text(draw, text, font, box_width):
    avg_char_width = sum(draw.textbbox((0, 0), c, font=font)[2] for c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ") / 52
    max_chars_per_line = max(1, int(box_width / avg_char_width))
    wrapped = textwrap.wrap(text, width=max_chars_per_line)
    return wrapped

def compose_card(template_path, name, message=None,
                 out_dir="static/cards", filename=None,
                 font_path_name="static/fonts/GreatVibes-Regular.ttf",
                 font_path_msg="static/fonts/font.ttf",
                 decor_rakhi="static/templates/rakhi1.png",
                 decor_flowers="static/templates/sweets1.png",
                 decor_sparkles="static/templates/tilak1.png"):

    if not filename:
        filename = f"{uuid.uuid4().hex}.png"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, filename)

    # Base template
    base = Image.open(template_path).convert("RGBA")
    W, H = base.size
    draw = ImageDraw.Draw(base)

    # Default message
    if not message:
        message = "On this Raksha Bandhan, may our bond of love grow stronger with every passing year!"

    # Load fonts
    name_font = ImageFont.truetype(font_path_name, size=int(H * 0.10))
    msg_font = ImageFont.truetype(font_path_msg, size=int(H * 0.045))

    # Warm gradient overlay
    gradient = Image.new("RGBA", base.size)
    for y in range(H):
        r = int(255 - (y / H) * 50)
        g = int(223 - (y / H) * 20)
        b = int(186 - (y / H) * 50)
        for x in range(W):
            gradient.putpixel((x, y), (r, g, b, 90))
    base = Image.alpha_composite(base, gradient)

    # Decorations
    for decor_path, pos, scale in [
        (decor_rakhi, (int(W*0.05), int(H*0.05)), 0.25),
        (decor_flowers, (int(W*0.75), int(H*0.02)), 0.22),
        (decor_sparkles, (0, 0), 1.0)
    ]:
        if os.path.exists(decor_path):
            decor = Image.open(decor_path).convert("RGBA")
            new_size = (int(W * scale), int(W * scale * decor.height / decor.width))
            decor = decor.resize(new_size, Image.LANCZOS)
            base.paste(decor, pos, decor)

    # Name (gold effect)
    name_lines = center_text(draw, name.strip(), name_font, box_width=int(W * 0.75))
    y = int(H * 0.35)
    for line in name_lines:
        bbox = draw.textbbox((0, 0), line, font=name_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # Shadow
        draw.text(((W - w) / 2 + 3, y + 3), line, font=name_font, fill=(150, 75, 0, 255))
        # Gold highlight
        draw.text(((W - w) / 2, y), line, font=name_font, fill=(255, 215, 0, 255))
        y += h + 5

    # Message
    msg_lines = center_text(draw, message, msg_font, box_width=int(W * 0.82))
    y = int(H * 0.55)
    for line in msg_lines:
        bbox = draw.textbbox((0, 0), line, font=msg_font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(((W - w) / 2, y), line, font=msg_font, fill=(60, 30, 10, 255))
        y += h + 6

    base.save(out_path, format="PNG")
    return out_path, filename
