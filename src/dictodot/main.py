from collections import OrderedDict

from typing import Generic
from typing import TypeVar

import numpy as np

DotDictKey = TypeVar("DotDictKey")
DotDictValue = TypeVar("DotDictValue")


class DotDict(OrderedDict, Generic[DotDictKey, DotDictValue]):
    """A simple dict using . for accession."""

    def __getattr__(self, key: DotDictKey) -> DotDictValue:
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")

    def __setattr__(self, key: DotDictKey, value: DotDictValue) -> None:
        self[key] = value

    def __delattr__(self, key: DotDictKey) -> None:
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'")

    @classmethod
    def Recursive(cls, dct):
        return cls(
            {k: cls.Recursive(v) if isinstance(v, dict) else v for k, v in dct.items()}
        )

    @classmethod
    def FromFrame(cls, df):
        return cls({k: v.to_numpy() for k, v in df.items()})


def test_DotDict():
    dct = {"a": "b"}
    dotted_dct = DotDict(dct)
    assert dotted_dct.a == dct["a"]


df2dd = lambda df: DotDict({c: df[c].to_numpy() for c in df})


def dd_zeros(shape, **name2dtype):
    import numpy as np

    return DotDict({name: np.zeros(shape, dtype) for name, dtype in name2dtype.items()})


def dd_empty(shape, **name2dtype):
    import numpy as np

    return DotDict({name: np.empty(shape, dtype) for name, dtype in name2dtype.items()})


def dd_full(shape, fill_value, **name2dtype):
    import numpy as np

    return DotDict(
        {name: np.full(shape, fill_value, dtype) for name, dtype in name2dtype.items()}
    )
