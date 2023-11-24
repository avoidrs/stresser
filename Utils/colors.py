from colorama import Fore, Style
from pystyle import Colors, Colorate, Center

class c:
    blue = Colors.blue
    red = Colors.red
    yellow = Colors.yellow
    green = Colors.green
    purple = Colors.purple
    cyan = Colors.cyan
    gray = Colors.gray
    orange = '\033[38;5;208m'
    lgreen = Colors.light_green
    lblue = Colors.light_blue
    lred = Colors.light_red
    lpurple = Fore.LIGHTMAGENTA_EX
    lyellow = Fore.LIGHTYELLOW_EX
    dblue = Colors.dark_blue
    dgray = Colors.dark_gray
    dgreen = Colors.dark_green
    dred = Colors.dark_red
    white = Colors.white

    bold = '\033[1m'
    underline = '\033[4m'
    italic = '\033[3m'
    reset = '\033[0m'