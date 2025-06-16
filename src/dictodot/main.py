from collections import OrderedDict

from typing import Generic
from typing import TypeVar


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
