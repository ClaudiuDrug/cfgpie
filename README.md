# cfgpie

Simplified `ConfigParser` setup.

This module automates, to some extent, the setup of [ConfigParser](https://docs.python.org/3.7/library/configparser.html)
with cmd-line args parsing ability.

---

#### Installation:

```commandline
python -m pip install [--upgrade] cfgpie
```

---

#### Usage:

After installation, simply import the class `CfgParser` from `cfgpie` module:
```python
from cfgpie import CfgParser
```

By passing a name with the `instance` param we can have multiple instances:
```python
# mymodule.py

from cfgpie import CfgParser

cfg = CfgParser(instance="main")
cfg2 = CfgParser(instance="main")
other = CfgParser(instance="other")


if __name__ == '__main__':
    
    print("*" * 80)
    print("cfg == other:", cfg == other)
    print("cfg is other:", cfg is other)

    print("*" * 80)
    print("cfg == cfg2:", cfg == cfg2)
    print("cfg is cfg2:", cfg is cfg2)
```

```
********************************************************************************
cfg == other: False
cfg is other: False
********************************************************************************
cfg == cfg2: True
cfg is cfg2: True
```

Setting up our config environment:

```python
# constants.py

from os.path import join, dirname, realpath
from sys import modules
from types import ModuleType

# main module:
MODULE: ModuleType = modules.get("__main__")

# root directory:
ROOT: str = dirname(realpath(MODULE.__file__))

# default config file path:
CONFIG: str = join(ROOT, "config", "config.ini")

# backup config params:
BACKUP: dict = {
    "FOLDERS": {
        "logger": r"${DEFAULT:directory}\logs",
    },
    "TESTS": {
        "option_1": "some_value",
        "option_2": 23453,
        "option_3": True,
        "option_4": r"${DEFAULT:directory}\value",  # extended interpolation
        "option_5": ["abc", 345, 232.545, "3534.5435", True, {"key_": "value_"}, False],
    },
}
```

For interpolation, refer to `interpolation-of-values`
[documentation](https://docs.python.org/3.7/library/configparser.html#interpolation-of-values).

```python
# mymodule.py

from cfgpie import CfgParser

from .constants import ROOT, CONFIG, BACKUP

cfg = CfgParser(instance="main")

# we can set default section options:
cfg.set_defaults(directory=ROOT)
# also possible at instance creation:
# cfg = CfgParser(defaults=some_dict)

# we can provide a backup dictionary
# in case our config file does not exist
# and by default a new file will be created
cfg.open(file_path=CONFIG, encoding="UTF-8", fallback=BACKUP)


if __name__ == '__main__':

    # we're parsing cmd-line arguments
    cfg.parse()

    print(cfg.get("TESTS", "option_1"))
    print(cfg.getint("TESTS", "option_2"))
```

This is also possible given that cmd-args are fetched as a list of strings:

```python
if __name__ == '__main__':
    cfg.parse(["--tests-option_1", "another_value", "--tests-option_2", "6543"])
    
    print(cfg.get("TESTS", "option_1"))
    print(cfg.getint("TESTS", "option_2"))
```

To pass cmd-line arguments:

```commandline
python -O main.py --section-option value --section-option value
```
cmd-line args have priority over config file and will override the cfg params.

Given that `CfgParser` inherits from `ConfigParser`, and with the help of our
converters, we now have seven extra methods to use in our advantage:

```python
some_list: list = cfg.getlist("SECTION", "option")
some_tuple: tuple = cfg.gettuple("SECTION", "option")
some_set: set = cfg.getset("SECTION", "option")
some_dict: dict = cfg.getdict("SECTION", "option")
some_path: str = cfg.getpath("SECTION", "option")

# these methods will also check if the path exists and create one if not. 
some_folder: str = cfg.getfolder("SECTION", "option")
some_file: str = cfg.getfile("SECTION", "option")
```

`getpath()`, `getfolder()` and `getfile()` also use `os.path.realpath`
to enforce a consistency in the formatting of the path.

If not provided, by default, `CfgParser` will set:

* `defaults` parameter as dict with section `DEFAULT` and option `directory` to the root folder of the `__main__` module.

* `instance` parameter to the name `default`;

* `interpolation` parameter to [ExtendedInterpolation](https://docs.python.org/3.7/library/configparser.html#configparser.ExtendedInterpolation);

* `converters` parameter to evaluate `list`, `tuple`, `set` and `dict` objects with the help of
    [ast.literal_eval()](https://docs.python.org/3.7/library/ast.html#ast.literal_eval) function.

    Plus `os.path.realpath()`, `folder()` and `file()` to evaluate paths.
    See [utils.py](src/cfgpie/utils.py) for the last two methods.
    > Note: `folder()` and `file()` methods will recursively create the folder structure if needed.

All other parameters are passed directly to
[ConfigParser](https://docs.python.org/3.7/library/configparser.html).

---
