_color_map = {
    "white": "37",
    "red": "91",
    "green": "92",
    "yellow": "93",
    "blue": "94",
    "purple": "95",
    "cyan": "96",
    "black": "30",
    "light_gray": "37",
    "dark_gray": "90",
    "light_red": "91",
    "light_green": "92",
    "light_yellow": "93",
    "light_blue": "94",
    "light_purple": "95",
    "light_cyan": "96",
    "default": "39"
}

_background_color_map = {
    "white": "107",
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "purple": "45",
    "cyan": "46",
    "light_gray": "47",
    "dark_gray": "100",
    "light_red": "101",
    "light_green": "102",
    "light_yellow": "103",
    "light_blue": "104",
    "light_purple": "105",
    "light_cyan": "106",
    "default": "49"
}

_style_map = {
    "bold": "1",
    "underline": "4",
    "blink": "5",
    "reverse": "7",
    "concealed": "8",
    "default": "0"
}

white = "white"
red = "red"
green = "green"
yellow = "yellow"
blue = "blue"
purple = "purple"
cyan = "cyan"
black = "black"
light_gray = "light_gray"
dark_gray = "dark_gray"
light_red = "light_red"
light_green = "light_green"
light_yellow = "light_yellow"
light_blue = "light_blue"
light_purple = "light_purple"
light_cyan = "light_cyan"

bold = "bold"
underline = "underline"
blink = "blink"
reverse = "reverse"
concealed = "concealed"


def printx(message, color="default", background_color="default", style="default"):
    if not isinstance(style, list):
        style = [style]

    for s in style:
        if s not in _style_map:
            style = ["default"]
            break

    styleCodeArr = [_style_map[c] for c in style]
    if color not in _color_map:
        color = "default"
    if background_color not in _background_color_map:
        background_color = "default"

    print(
        f'\033[{';'.join(styleCodeArr)};{_background_color_map[background_color]};{_color_map[color]}m{message}\033[0m')
