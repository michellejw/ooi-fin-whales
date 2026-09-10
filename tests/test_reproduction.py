"""The constitution's reproduction gate, as a check that runs.

If this stops passing, the measurement path has drifted away from the 2017
study and every comparison built on it is suspect. Established in
``notes/probes/06-fig7-reproduction.md``.

The archive lives in ``data/``, which is gitignored, so these skip rather than
fail on a machine that has not fetched it. Restore it with the commit and
checksums in ``manifests/ground-truth-fin-call-patterns.json``.
"""

import csv
from pathlib import Path

import numpy as np
import pytest

from ooi_fin_whales.archive import NOTE_A_MAX_HZ, SINGLET_MIN_IPI_S, season_peak

REPO = Path(__file__).resolve().parent.parent
ARCHIVE = REPO / "data" / "fin-call-patterns"
KEMF_2011 = ARCHIVE / "DETECTION_DATA" / "KEMF_2011_2012.h5"
YEARLY = ARCHIVE / "SEQ_CODE" / "ALL_seq_YEARLY_4nov2016_5dBthresh_kurtosis.csv"

needs_archive = pytest.mark.skipif(
    not ARCHIVE.exists(),
    reason="ground-truth archive not present; see manifests/ for how to restore it",
)

# One histogram bin: 0.1 Hz on frequency, 0.5 s on IPI.
FREQ_TOL_HZ = 0.1
IPI_TOL_S = 0.5


@needs_archive
def test_kemf_2011_matches_the_archived_summary():
    """Recomputing from per-note data reproduces the study's own season peak."""
    got = season_peak(KEMF_2011)
    assert got["frequency_hz"] == pytest.approx(19.2, abs=FREQ_TOL_HZ), (
        f"frequency peak {got['frequency_hz']:.2f} Hz, archived summary says 19.2. "
        "A miss of several Hz usually means the note-A threshold was not applied "
        "and the taller B-note mode won."
    )
    assert got["ipi_s"] == pytest.approx(28.5, abs=IPI_TOL_S), (
        f"IPI peak {got['ipi_s']:.2f} s, archived summary says 28.5. "
        "A value near 14 s means the singlet threshold was not applied and the "
        "doublet population won."
    )


def _dominant_singlet_a_peaks():
    """Per station-season singlet A-note peaks, on the three trend instruments."""
    best: dict[tuple[str, str], tuple[float, float, float]] = {}
    with YEARLY.open() as f:
        for row in csv.DictReader(f):
            st, date = row["station"], row["datevec"]
            freq, ipi = float(row["freq"]), float(row["ipi"])
            counts = float(row["peakcounts"])
            if st not in {"AX", "KENE", "KEMF"} or counts <= 0:
                continue
            if ipi <= SINGLET_MIN_IPI_S or freq >= NOTE_A_MAX_HZ:
                continue
            key = (st, date)
            if key not in best or counts > best[key][2]:
                best[key] = (freq, ipi, counts)
    # The paper notes the singlet had essentially disappeared by 2012-13.
    return {k: v for k, v in best.items() if not (k[0] == "AX" and k[1][:4] == "2012")}


@needs_archive
def test_decadal_ipi_trend_matches_the_published_fit():
    """The published +0.54 s/yr at R2 0.96 comes back out of the archive."""
    peaks = _dominant_singlet_a_peaks()
    years = np.array([int(d[:4]) for _, d in peaks], dtype=float)
    ipi = np.array([v[1] for v in peaks.values()])

    slope, _ = np.polyfit(years, ipi, 1)
    r2 = np.corrcoef(years, ipi)[0, 1] ** 2

    assert slope == pytest.approx(0.54, abs=0.05), (
        f"IPI trend {slope:+.3f} s/yr, published +0.54"
    )
    assert r2 == pytest.approx(0.96, abs=0.02), f"IPI R2 {r2:.2f}, published 0.96"
