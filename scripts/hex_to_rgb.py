"""Python script that replaces hexidecimal colors with RGB colors in files"""

import re
import sys


def hex_to_rgb(hex_color: str):
    """Converts hexidecimal color to RGB color"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def replace_hex(match):
    """Replaces hexidecimal color with RGB color"""
    hex_color = match.group(0)
    rgb_color = hex_to_rgb(hex_color)
    return " ".join(str(color) for color in rgb_color)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python hex_to_rgb.py <file>")
        sys.exit(1)

    file_name = sys.argv[1]
    with open(file_name, "r") as file:
        file_contents = file.read()

    file_contents = re.sub(r"#[0-9a-fA-F]{6}", replace_hex, file_contents)

    with open(file_name, "w") as file:
        file.write(file_contents)


if __name__ == "__main__":
    main()
