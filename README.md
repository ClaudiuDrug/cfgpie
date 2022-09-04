# cfgpie

Simplified `ConfigParser` setup.

This module automates, to some extent, the setup of `ConfigParser` with cmd-line args parsing ability.

---

#### Installation:

```commandline
python -m pip install [--upgrade] cfgpie
```

---

#### Usage:

```python
# your 'main.py' module

from os.path import join, dirname, realpath
from sys import modules
from types import ModuleType

from cfgpie import get_config, CfgParser

# ***************************** config constants: **************************** #

# main module
MODULE: ModuleType = modules.get("__main__")

# root directory
ROOT: str = dirname(realpath(MODULE.__file__))

# default config file path:
CONFIG: str = join(ROOT, "config", "cfgpie.ini")

# backup config params:
BACKUP: dict = {
    "SECTION_1": {
        "option_1": "one",
        "option_2": 2,
        # extended interpolation (refer to `ConfigParser` documentation):
        "option_3": r"${DEFAULT:directory}\value",
    },
}

# NOTE: The constants above serve the usage example
#       and you can use whatever suits you best.

# *********************** get `ConfigParser` instance: *********************** #

# by passing a value to `name` param,
# we can have more named instances:
cfg: CfgParser = get_config(name="root")

# we can set default section options:
cfg.set_defaults(directory=ROOT)

# we can provide a backup dictionary
# in case our config file does not exist
# and a new one will be created
cfg.open(file_path=CONFIG, encoding="UTF-8", fallback=BACKUP)


if __name__ == '__main__':

    # we're parsing cmd-line arguments
    cfg.parse()

    print(cfg.get("SECTION_1", "option_1"))
    print(cfg.getint("SECTION_1", "option_2"))
    print(cfg.get("SECTION_1", "option_3"))
```

We can also do this:

```python
if __name__ == '__main__':
    cfg.parse(["--section_1-option_1", "1", "--section_1-option_2", "two"])
    
    print(cfg.getint("SECTION_1", "option_1"))
    print(cfg.get("SECTION_1", "option_2"))
    print(cfg.get("SECTION_1", "option_3"))
```

To pass cmd-line arguments:

```commandline
python -O main.py --section-option value --section-option value
```
cmd-line args have priority over config file and will override the cfg params.

Given that `CfgParser` inherits from `ConfigParser`, and with the help of our
converters, we now have four extra methods to use in our advantage:

```python
some_list = cfg.getlist("SECTION", "option")
some_tuple = cfg.gettuple("SECTION", "option")
some_set = cfg.getset("SECTION", "option")
some_dict = cfg.getdict("SECTION", "option")
```

If not provided, by default, `get_config` will set:
* `name` parameter to the name of the module from which is called (see `constants.py` for `MODULE`)
* `interpolation` parameter to `ExtendedInterpolation`;
* `converters` parameter to evaluate `list`, `tuple`, `set` and `dict` objects with the help of `evaluate` function (see `utils.py`).

All other parameters are passed directly to `CfgParser` (see `configparser` [documentation](https://docs.python.org/3.10/library/configparser.html)).

---
