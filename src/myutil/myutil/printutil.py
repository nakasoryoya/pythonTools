_COLOR_MAP = {
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

_BACKGROUND_COLOR_MAP = {
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

_STYLE_MAP = {
    "bold": "1",
    "underline": "4",
    "blink": "5",
    "reverse": "7",
    "concealed": "8",
    "default": "0"
}

WHITE = "white"
RED = "red"
GREEN = "green"
YELLOW = "yellow"
BLUE = "blue"
PURPLE = "purple"
CYAN = "cyan"
BLACK = "black"
LIGHT_GRAY = "light_gray"
DARK_GRAY = "dark_gray"
LIGHT_RED = "light_red"
LIGHT_GREEN = "light_green"
LIGHT_YELLOW = "light_yellow"
LIGHT_BLUE = "light_blue"
LIGHT_PURPLE = "light_purple"
LIGHT_CYAN = "light_cyan"

BOLD = "bold"
UNDERLINE = "underline"
BLINK = "blink"
REVERSE = "reverse"
CONCEALED = "concealed"


def printx(message: str, color: str = "default", background_color: str = "default", style="default"):
    if not isinstance(style, list):
        style = [style]

    for s in style:
        if s not in _STYLE_MAP:
            style = ["default"]
            break

    styleCodeArr = [_STYLE_MAP[c] for c in style]

    print(
        f'\033[{';'.join(styleCodeArr)};'
        f'{_BACKGROUND_COLOR_MAP.get(background_color, _BACKGROUND_COLOR_MAP["default"])};'
        f'{_COLOR_MAP.get(color, _COLOR_MAP["default"])}m{message}\033[0m')
