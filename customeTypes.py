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
    COMMAND = 1
    INSERT = 2

class SITE(Enum):
    FCHAN  = 0
    REDDIT = 1

class STICKIES(Enum):
    SHOW = 0
    HIDE = 1