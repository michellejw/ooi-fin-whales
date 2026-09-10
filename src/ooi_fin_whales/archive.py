"""Read the 2017 study's archived per-note detections.

The files are pandas HDFStore *fixed-format* frames written by pandas 0.15.2,
not plain HDF5 tables, so h5py cannot read them column by column. Each frame
stores its column names in ``df/axis0`` and its data in a handful of
``df/blockN_values`` arrays grouped by dtype, with ``df/blockN_items`` naming
the columns each block holds. :func:`read_station_season` walks that mapping so
that nothing here depends on a block index, which is not stable across files.

Two columns need decoding rather than reading. ``dettime`` is ``datetime64[ns]``
UTC stored as ``int64``, and ``ipi`` is ``timedelta64[ns]`` stored the same way.
A third, ``station``, is a pickled object array; it is not decoded here because
the filename carries the same information without the pickle.

The selection constants below are the reason a naive read of these files does
not reproduce the published numbers. Both the frequency and the IPI
distributions are bimodal, and in both cases the *wrong* mode is taller, so a
global argmax returns the B note and the doublet interval while looking
entirely reasonable. See ``notes/probes/06-fig7-reproduction.md``.
"""

from __future__ import annotations

from pathlib import Path

import h5py
import numpy as np

# From the paper's Methods.
SINGLET_MIN_IPI_S = 22.0
"""A singlet note follows the previous note by more than this. Below it, doublet."""

NOTE_A_MAX_HZ = 22.0
"""Note A sits below this frequency. Note B sits above it."""

# From the archived analysis code, SEQ_CODE/AX_CZ-1DHISTOS.py.
MAX_IPI_S = 60.0
MIN_SNR_DB = 5.0
MIN_SEQUENCE_NOTES = 10

# Histogram bins, also from the archived analysis code.
FREQ_BINS = (17.0, 23.0, 0.1)
IPI_BINS = (10.0, 40.0, 0.5)

_NS_PER_S = 1e9
_BLOCK_NDIM = 2  # rows by columns; the pickled object block is not this shape


def read_station_season(path: str | Path) -> dict[str, np.ndarray]:
    """Return the per-note table as a dict of columns.

    Keys are the archive's own column names. ``dettime`` comes back as
    ``datetime64[ns]`` and ``ipi`` as float seconds; everything else keeps its
    stored dtype. ``station`` is omitted, being a pickled object array. Take it
    from the filename.
    """
    out: dict[str, np.ndarray] = {}
    with h5py.File(Path(path), "r") as f:
        g = f["df"]
        for key in g:
            if not key.endswith("_items"):
                continue
            block = key[: -len("_items")]
            names = [n.decode() for n in g[key][...]]
            values = g[f"{block}_values"]
            # The pickled object block has no usable numeric shape.
            if values.dtype == object or values.ndim != _BLOCK_NDIM:
                continue
            data = values[...]
            for col, name in enumerate(names):
                out[name] = data[:, col]

    if "dettime" in out:
        out["dettime"] = out["dettime"].astype("int64").view("datetime64[ns]")
    if "ipi" in out:
        out["ipi"] = out["ipi"].astype("float64") / _NS_PER_S
    return out


def in_long_sequences(seqnum: np.ndarray, keep: np.ndarray) -> np.ndarray:
    """Restrict ``keep`` to notes in sequences of more than ``MIN_SEQUENCE_NOTES``.

    Sequence length is counted over the notes already selected by ``keep``,
    which is what the archived code does: it filters first, then measures the
    sequences that survive.
    """
    lengths = {}
    kept = seqnum[keep]
    uniq, counts = np.unique(kept, return_counts=True)
    lengths.update(zip(uniq.tolist(), counts.tolist(), strict=True))
    long_enough = np.array(
        [lengths.get(s, 0) > MIN_SEQUENCE_NOTES for s in kept], dtype=bool
    )
    out = keep.copy()
    out[keep] = long_enough
    return out


def select_notes(
    table: dict[str, np.ndarray],
    *,
    singlet: bool = True,
    note_a: bool = True,
) -> np.ndarray:
    """Boolean mask for the notes the 2017 analysis would have used.

    The house recipe is always applied: in sequence, IPI below
    ``MAX_IPI_S``, SNR above ``MIN_SNR_DB``, and a sequence longer than
    ``MIN_SEQUENCE_NOTES`` notes. ``singlet`` and ``note_a`` add the paper's
    two definitional thresholds and default to the combination the published
    trend was fitted on.
    """
    keep = (
        table["isseq"].astype(bool)
        & (table["ipi"] < MAX_IPI_S)
        & (table["snr"] > MIN_SNR_DB)
    )
    keep = in_long_sequences(table["seqnum"], keep)
    if singlet:
        keep &= table["ipi"] > SINGLET_MIN_IPI_S
    if note_a:
        keep &= table["frequency"] < NOTE_A_MAX_HZ
    return keep


def histogram_peak(values: np.ndarray, bins: tuple[float, float, float]) -> float:
    """Centre of the fullest bin, over ``(low, high, width)``.

    Returns ``nan`` when nothing falls in range, rather than raising, so that a
    season with no usable notes is a missing value rather than a crash.
    """
    low, high, width = bins
    v = values[np.isfinite(values) & (values >= low) & (values <= high)]
    if v.size == 0:
        return float("nan")
    edges = np.arange(low, high + width, width)
    counts, _ = np.histogram(v, bins=edges)
    return float((edges[:-1] + width / 2)[counts.argmax()])


def season_peak(path: str | Path) -> dict[str, float]:
    """Frequency and IPI peaks for one station-season, singlet A notes."""
    table = read_station_season(path)
    keep = select_notes(table)
    return {
        "frequency_hz": histogram_peak(table["frequency"][keep], FREQ_BINS),
        "ipi_s": histogram_peak(table["ipi"][keep], IPI_BINS),
        "n_notes": int(keep.sum()),
    }
