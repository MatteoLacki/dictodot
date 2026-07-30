import os
from pathlib import Path
import subprocess
import sys

import pytest

from dictodot import DotDict
from dictodot import dd_empty
from dictodot import dd_full
from dictodot import dd_zeros


def test_base_package_imports_without_site_packages():
    project_root = Path(__file__).parent.parent
    env = dict(os.environ)
    env["PYTHONPATH"] = str(project_root / "src")

    subprocess.run(
        [
            sys.executable,
            "-S",
            "-c",
            "from dictodot import DotDict; assert DotDict({'value': 1}).value == 1",
        ],
        check=True,
        env=env,
    )


def test_numpy_allocation_helpers():
    np = pytest.importorskip("numpy")

    arrays = dd_zeros((2, 3), counts=np.int64)
    assert isinstance(arrays, DotDict)
    np.testing.assert_array_equal(arrays.counts, np.zeros((2, 3), dtype=np.int64))

    arrays = dd_empty((2,), scores=np.float64)
    assert arrays.scores.shape == (2,)
    assert arrays.scores.dtype == np.float64

    arrays = dd_full((2,), 7, labels=np.int32)
    np.testing.assert_array_equal(arrays.labels, np.full((2,), 7, dtype=np.int32))
