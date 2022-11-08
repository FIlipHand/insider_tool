from enum import Enum


class StyleChoice(str, Enum):
    short = 'short'
    normal = 'normal'
    full = 'full'


class TitleChoice(str, Enum):
    officer = 'officer'
    COB = 'COB'
    CEO = 'CEO'
    Pres = 'Pres'
    COO = 'COO'
    CFO = 'CFO'
    GC = 'GC'
    VP = 'VP'
    Director = 'Director'
    ten_own = '10own'
    other = 'other'
