import os
import pytest
from pathlib import Path

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
  f"--cov-fail-under={COV_FAIL_UNDER}"
]

os.environ["YARN_CACHE_FOLDER"] = str(CACHE_DIR)

for cmd in [
  ["yarn"],
  ["yarn", "lerna", "bootstrap"],
  ["yarn", "build"],
]:
    rc = subprocess.call(cmd, cwd=str(SRC))
    if rc:
        print("FAIL on", cmd)
        sys.exit(rc)

sys.exist(pytest.main(pytest_args), cwd=str(SRC))