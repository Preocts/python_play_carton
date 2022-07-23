"""
https://pingperfect.com/index.php/knowledgebase/971/Ark-Survival-Evolved--How-to-change-Engram-Points-Earned.html

Egg.
"""
import re

CLEAN_RE = re.compile(r"\s")
MAX_LEVELS = 180
DEFAULT_EXP = 0
SECTION_NAME = "OverridePlayerLevelEngramPoints"
FILENAME = "ark_exp_map.ini"

# [range]:[amount]
# 1:10 sets level 1 to 10
# 1, 4, 8:10 set levels 1, 4 and 8 to 10
# 49-87:10 set levels 49 through 87 to 10
# Processed top to bottom, overrights existing
exp_bonuses = [
    "1-15:15",
    "16-100:20",
    "14, 25, 39, 23: 69",  # Nice levels
    "101 - 180: 1",  # Let the grind begin rooH
]

bonus_map = {idx: DEFAULT_EXP for idx in range(1, MAX_LEVELS + 1)}

for section in exp_bonuses:
    # clean
    clean_sec = CLEAN_RE.sub("", section)

    # this will helpfully error if invalid format
    levels, amount = clean_sec.split(":")

    # Get a list
    if "-" in levels:
        start, stop = levels.split("-")
        level_range = list(range(int(start), int(stop) + 1))
    elif "," in levels:
        level_range = [int(lvl) for lvl in levels.split(",")]
    else:
        level_range = [int(levels)]

    for lr in level_range:
        bonus_map[lr] = int(amount)

lines = [f"{SECTION_NAME}={value}" for value in bonus_map.values()]
with open(FILENAME, "w") as outfile:
    outfile.write("\n".join(lines))
