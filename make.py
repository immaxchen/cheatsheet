import json
from os import listdir
from os.path import isdir

with open("menu.json", "w") as fp:
    json.dump(
        {
            d: sorted(listdir(d))
            for d in listdir()
            if isdir(d) and not d.startswith(".")
        },
        fp,
        sort_keys=True,
        indent=4,
    )
