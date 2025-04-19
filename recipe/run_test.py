import os
from pathlib import Path
import sys
from subprocess import call

COV_FAIL_UNDER = 81
HERE = Path(__file__).parent

SRC = HERE / "src"
YARN_RC = SRC / ".yarnrc.yml"
YARN_RC_TEXT = """
enableImmutableInstalls: false
enableInlineBuilds: false
enableTelemetry: false
nodeLinker: node-modules
logFilters:
  - {level: discard, code: YN0006} # SOFT_LINK_BUILD
  - {level: discard, code: YN0007} # MUST_BUILD
  - {level: discard, code: YN0008} # MUST_REBUILD
  - {level: discard, code: YN0013} # FETCH_NOT_CACHED
  - {level: discard, code: YN0019} # UNUSED_CACHE_ENTRY
"""
COV_RUN = ["coverage", "run", "--source=jupyter_ydoc", "--branch", "-m"]
PYTEST = ["pytest", "-vv", "--asyncio-mode=auto", "--color=yes", "--tb=long"]
COV_REPORT = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COV_FAIL_UNDER}",
]


def do(*args: str) -> int:
    print(">>>", *args)
    return call(args, cwd=str(SRC))


if __name__ == "__main__":
    os.environ.update(YARN_CACHE_FOLDER=str(HERE / ".yarn-cache"))
    YARN_RC.write_text(YARN_RC_TEXT, encoding="utf-8")
    sys.exit(
        do("yarn") or do("yarn", "build") or do(*COV_RUN, *PYTEST) or do(*COV_REPORT)
    )
