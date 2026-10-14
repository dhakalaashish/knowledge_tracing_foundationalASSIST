def print_with_color(text, color=None):
    """
    彩色打印文本（支持7种颜色）

    参数:
        text: 要打印的文本
        color: 颜色名称（red/green/yellow/blue/purple/cyan/white）
    """
    color_codes = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }

    reset_code = '\033[0m'

    if color and color.lower() in color_codes:
        print(f"{color_codes[color.lower()]}{text}{reset_code}")
    else:
        print(text)
