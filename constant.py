import os
import sys


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


FILE_PATH_SUBCORE = resource_path("JSON/subcore.json")
FILE_PATH_LEG = resource_path("JSON/parts_leg.json")
FILE_PATH_BODY = resource_path("JSON/parts_body.json")
FILE_PATH_WEAPON = resource_path("JSON/parts_weapon.json")
FILE_PATH_ACC = resource_path("JSON/parts_acc.json")

LEG = 1
BODY = 2
WEAPON = 3
ACC = 4

SAGITTARIUS = 9
