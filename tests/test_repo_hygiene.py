"""Guards on what may enter the repository.

These are not tests of the science. They exist because the failure they catch
is silent and permanent: a per-note table committed once stays in git history
forever, and nobody notices until the clone is slow.

The size rule follows from the granularity split documented in
results/README.txt and work/README.txt. One row per season is kilobytes. One
row per note is megabytes and belongs in work/, which is gitignored and
destined for a Zenodo archive instead.
"""

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent

# A season's histogram peaks are a few dozen rows. A season's per-note
# detections are 5-10 MB. 1 MB sits well clear of the first and well below
# the second, so anything that trips it is a granularity mistake, not growth.
MAX_RESULT_BYTES = 1_000_000


def _tracked_files(directory: Path) -> list[Path]:
    """Files git would actually commit, ignoring anything gitignored."""
    out = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", str(directory)],
        cwd=REPO, capture_output=True, text=True, check=True,
    )
    return [REPO / line for line in out.stdout.splitlines() if line]


def test_results_files_stay_small():
    """results/ holds per-season summaries, so nothing in it should be large."""
    oversized = [
        (p.relative_to(REPO), p.stat().st_size)
        for p in _tracked_files(REPO / "results")
        if p.is_file() and p.stat().st_size > MAX_RESULT_BYTES
    ]
    assert not oversized, (
        "Files in results/ exceed the size limit:\n"
        + "\n".join(f"  {p} is {n:,} bytes" for p, n in oversized)
        + f"\n\nLimit is {MAX_RESULT_BYTES:,} bytes. This almost always means "
        "per-note data landed in results/. Move it to work/, which is "
        "gitignored, and commit a per-season summary instead."
    )


@pytest.mark.parametrize("directory", ["data", "work"])
def test_bulk_directories_are_gitignored(directory):
    """data/ and work/ must stay ignored, or a season's output lands in git."""
    probe = REPO / directory / ".hygiene-probe"
    probe.parent.mkdir(exist_ok=True)
    probe.touch()
    try:
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", str(probe)], cwd=REPO
        ).returncode == 0
    finally:
        probe.unlink()
    assert ignored, (
        f"{directory}/ is not gitignored. A single season of frame "
        f"probabilities is roughly 18 GB; committing it is unrecoverable "
        f"without rewriting history. Restore the entry in .gitignore."
    )


@pytest.mark.parametrize("directory", ["data", "work"])
def test_bulk_directory_readmes_survive_the_ignore(directory):
    """The README inside an ignored directory must still be committable.

    Regression test. `.gitignore` originally read `work/` and `data/`, which
    ignore the directory itself and everything under it. That silently took
    the README explaining what belongs there, so the rule was documented in a
    file nobody cloning the repo would ever receive. The fix is the `dir/*`
    plus `!dir/README.txt` form, and this test is here so it stays that way.
    """
    readme = REPO / directory / "README.txt"
    assert readme.exists(), f"{directory}/README.txt is missing"
    ignored = subprocess.run(
        ["git", "check-ignore", "-q", str(readme)], cwd=REPO
    ).returncode == 0
    assert not ignored, (
        f"{directory}/README.txt is gitignored, so the rule it documents will "
        f"not reach anyone who clones this repository. .gitignore needs the "
        f"`{directory}/*` plus `!{directory}/README.txt` form, not a bare "
        f"`{directory}/`."
    )
