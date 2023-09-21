import os
import sys
import subprocess
from pathlib import Path

import pytest

COV_FAIL_UNDER = 70

HERE = Path(__file__).parent
SRC = HERE / "src"
CACHE_DIR = Path(os.environ["SRC_DIR"]) / ".yarn-cache"
PYTEST_ARGS = [
    "-vv",
    "--asyncio-mode=auto",
    "--cov=jupyter_ydoc",
    "--cov-report=term-missing:skip-covered",
    "--no-cov-on-fail",
    f"--cov-fail-under={COV_FAIL_UNDER}",
]

os.environ.update(
    YARN_CACHE_FOLDER=str(CACHE_DIR),
    YARN_ENABLE_IMMUTABLE_INSTALLS="false",
)

for cmd in [
    ["yarn"],
    ["yarn", "lerna", "bootstrap"],
    ["yarn", "build"],
]:
    rc = subprocess.call(cmd, cwd=str(SRC))
    if rc:
        print("FAIL on", cmd)
        sys.exit(rc)

sys.exist(pytest.main(PYTEST_ARGS), cwd=str(SRC))
