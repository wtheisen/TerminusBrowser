from enum import Enum

class VIEWSTYLES(Enum):
    BOXES   = 0
    TREE    = 1
    CASCADE = 2

class LEVEL(Enum):
    INDEX  = 0
    BOARD  = 1
    THREAD = 2

class MODE(Enum):
    NORMAL = 0
    INSERT = 1