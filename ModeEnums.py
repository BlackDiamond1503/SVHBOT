from enum import Enum
from ModeData import ModeData

class GameModeType(Enum):
    SVH=ModeData("SVH","svh","**Standard hunt**")
    ROULETTE=ModeData("ROULETTE","roulette","**Roulette run**")
    TWIST=ModeData("TWIST","twist","**Twist hunt**")
    ANY=ModeData("ANY","any","**Hunt** of any modality")
    
class GameType(Enum):
    HK=ModeData("HK","hk","Hallownest")
    SS=ModeData("SS","ss","Pharloom")
    ANY=ModeData("ANY","any","Hallownest or Pharloom")