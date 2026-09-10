"""Reproduce the 2017 study's published numbers from its own archived detections.

Run with:  uv run marimo edit notebooks/01_reproduce_2017.py --port 2722
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        # Reproducing the 2017 fin whale results

        The 2017 study measured two things about the 20 Hz fin whale call and
        found both were changing over a decade: the gap between pulses (IPI)
        grew longer, and the call's frequency dropped.

        It published its per-note detections, so we can recompute its results
        rather than take them on trust. That is what this notebook does, and it
        is the foundation everything else in the project rests on: we cannot
        measure how a *new* detector differs from the old one unless we can
        first reproduce what the old one reported.

        Nothing here is downloaded. It reads the pinned archive in `data/`.
        """
    )
    return


@app.cell
def _():
    from pathlib import Path

    import marimo as mo
    import numpy as np

    from ooi_fin_whales import archive

    KEMF_2011 = Path("data/fin-call-patterns/DETECTION_DATA/KEMF_2011_2012.h5")
    table = archive.read_station_season(KEMF_2011)
    return KEMF_2011, archive, mo, np, table


@app.cell(hide_code=True)
def _(mo, table):
    mo.md(
        f"""
        ## What is in the file

        One row per detected note, **{len(table["dettime"]):,}** of them, covering
        the 2011-2012 season at station KEMF on the Endeavour segment.

        The columns that matter here:

        - `frequency` the note's pitch in Hz
        - `ipi` seconds since the previous note
        - `isseq` whether the note is part of a song sequence
        - `snr` signal-to-noise ratio in dB
        - `seqnum` which sequence the note belongs to
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## The obvious approach, and why it is wrong

        The published value for this season is about **19.2 Hz** and
        **28.5 seconds**. The obvious way to get there is to take the most
        common value of each. Try it.
        """
    )
    return


@app.cell
def _(archive, np, table):
    # A wider band than archive.FREQ_BINS, which is the study's analysis band
    # and would clip the peak we are about to find at its upper edge.
    naive_freq = archive.histogram_peak(table["frequency"], (15.0, 30.0, 0.1))
    naive_ipi = archive.histogram_peak(
        table["ipi"][np.isfinite(table["ipi"])], (5.0, 60.0, 0.5)
    )
    naive_freq, naive_ipi
    return naive_freq, naive_ipi


@app.cell(hide_code=True)
def _(mo, naive_freq, naive_ipi):
    mo.md(
        f"""
        That gives **{naive_freq:.2f} Hz** and **{naive_ipi:.2f} s**, against a
        published 19.2 and 28.5. Both are wrong, and neither is wrong by a
        little.

        The plot below shows why.
        """
    )
    return


@app.cell(hide_code=True)
def _(np, table):
    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 3.5))

    f = table["frequency"][np.isfinite(table["frequency"])]
    ax1.hist(f, bins=np.arange(15, 30, 0.25), color="#4C72B0")
    ax1.axvline(22.0, color="crimson", ls="--", label="note A / note B at 22 Hz")
    ax1.set_xlabel("frequency (Hz)")
    ax1.set_ylabel("notes")
    ax1.set_title("Two notes, not one")
    ax1.legend(fontsize=8)

    i = table["ipi"][np.isfinite(table["ipi"])]
    ax2.hist(i[(i > 5) & (i < 60)], bins=np.arange(5, 60, 0.5), color="#55A868")
    ax2.axvline(22.0, color="crimson", ls="--", label="doublet / singlet at 22 s")
    ax2.set_xlabel("inter-pulse interval (s)")
    ax2.set_title("Two song types, not one")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        Each distribution has **two humps**, and in both cases the taller hump
        is the one we do not want.

        Fin whales here sing two notes, a lower **A** note and a higher **B**
        note, and the paper splits them at 22 Hz. They also sing in two
        patterns: **singlets**, one note every 25 seconds or so, and
        **doublets**, note pairs with a short gap inside each pair. The paper
        splits those at 22 seconds.

        The decadal trend was fitted on **singlet A notes** only. Taking the
        most common value across everything answers a different question.

        There is one more filter, which comes from the study's own analysis
        code rather than the paper: keep notes in sequence, with IPI under 60 s,
        SNR above 5 dB, in sequences longer than 10 notes. That drops isolated
        detections and noise.
        """
    )
    return


@app.cell
def _(KEMF_2011, archive):
    result = archive.season_peak(KEMF_2011)
    result
    return (result,)


@app.cell(hide_code=True)
def _(mo, result):
    freq_ok = abs(result["frequency_hz"] - 19.2) <= 0.1
    ipi_ok = abs(result["ipi_s"] - 28.5) <= 0.5
    mo.md(
        f"""
        ## The answer

        | | recomputed | study's own summary |
        |---|---|---|
        | frequency | {result["frequency_hz"]:.2f} Hz | 19.2 Hz |
        | IPI | {result["ipi_s"]:.2f} s | 28.5 s |

        Based on **{result["n_notes"]:,}** singlet A notes.

        {"Both match to within one histogram bin." if freq_ok and ipi_ok else "**These do not match. Something is wrong.**"}

        The archived per-note files regenerate the study's published season
        values. That is what makes the rest of the project possible.
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
        ## Still open

        Refitting the whole decade this way returns the published IPI trend
        exactly: **+0.534 s/yr at an R-squared of 0.96**, against a published
        +0.54 at 0.96. `tests/test_reproduction.py` checks this on every run.

        Frequency is a different story. The slope comes back right, -0.175 Hz/yr
        against a published -0.17, but the R-squared does not: **0.74 against a
        published 0.86**. So the paper selected the seasons or the notes for its
        frequency fit slightly differently than we do here, and nobody has
        worked out how.

        That is a real open question and a good first one. The data is all in
        `data/fin-call-patterns/SEQ_CODE/ALL_seq_YEARLY_4nov2016_5dBthresh_kurtosis.csv`,
        and `notes/probes/06-fig7-reproduction.md` records everything tried so far.
        """
    )
    return


if __name__ == "__main__":
    app.run()
