"""Seven stations, one season: what explains the KEMF frequency offset?

Writes results/stations_2011_2012.csv. The write-up is
notes/probes/07-kemf-offset-seven-stations.md.

Run with:  uv run marimo edit notebooks/02_station_comparison.py --port 2722
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Seven stations, one season

    Probe 6 found KEMF reading about 0.8 Hz higher than Axial in 2011-2012,
    with identical IPI, and listed candidate explanations without testing
    them. Seven stations recorded that season. If the offset follows sensor
    type, depth or sample rate, it should show up across them.
    """)
    return


@app.cell
def _():
    import csv
    from pathlib import Path

    import marimo as mo

    from ooi_fin_whales import archive

    DETECTIONS = Path("data/fin-call-patterns/DETECTION_DATA")
    RESULTS = Path("results/stations_2011_2012.csv")

    # From the 2017 paper's Table 1, transcribed in
    # notes/literature/2017-paper-data-section.md.
    STATIONS = {
        "AX": ("hydrophone", 1550, 100),
        "KEMF": ("seismometer", 2205, 100),
        "J63A": ("seismometer", 2880, 50),
        "J23A": ("seismometer", 2660, 50),
        "J06A": ("seismometer", 3220, 50),
        "G30A": ("seismometer", 3120, 50),
        "G03A": ("seismometer", 4110, 50),
    }
    return DETECTIONS, RESULTS, STATIONS, archive, csv, mo


@app.cell
def _(DETECTIONS, STATIONS, archive):
    tables = {
        st: archive.read_station_season(DETECTIONS / f"{st}_2011_2012.h5")
        for st in STATIONS
    }

    rows = []
    for _st, (_sensor, _depth, _rate) in STATIONS.items():
        _r = archive.season_peak(DETECTIONS / f"{_st}_2011_2012.h5")
        rows.append(
            {
                "station": _st,
                "sensor": _sensor,
                "depth_m": _depth,
                "sample_rate_hz": _rate,
                "frequency_hz": round(_r["frequency_hz"], 2),
                "ipi_s": round(_r["ipi_s"], 2),
                "n_notes": _r["n_notes"],
            }
        )
    return rows, tables


@app.cell
def _(RESULTS, csv, mo, rows):
    with RESULTS.open("w", newline="") as _f:
        _w = csv.DictWriter(_f, fieldnames=list(rows[0]), lineterminator="\n")
        _w.writeheader()
        _w.writerows(rows)

    mo.vstack([mo.md(f"Written to `{RESULTS}`."), mo.ui.table(rows, selection=None)])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Does the offset depend on how loud the note is?

    The frequency is an amplitude-weighted centroid over 15-35 Hz. A quiet
    note sits closer to the noise floor, so background noise carries more of
    the weight. If KEMF's noise is louder at higher frequencies, its quiet
    notes would read high. Bin each station's singlet A notes by SNR and take
    the frequency peak in each bin.
    """)
    return


@app.cell
def _(archive, mo, tables):
    SNR_BINS = [(5, 8), (8, 11), (11, 15), (15, 20), (20, 99)]

    snr_rows = []
    for _st, _t in tables.items():
        _keep = archive.select_notes(_t)
        _row = {"station": _st}
        for _lo, _hi in SNR_BINS:
            _m = _keep & (_t["snr"] >= _lo) & (_t["snr"] < _hi)
            _peak = archive.histogram_peak(_t["frequency"][_m], archive.FREQ_BINS)
            _row[f"{_lo}-{_hi} dB"] = (
                f"{_peak:.2f} (n={int(_m.sum())})" if _m.sum() >= 100 else "-"
            )
        snr_rows.append(_row)
    mo.ui.table(snr_rows, selection=None)
    return


@app.cell
def _(archive, mo, tables):
    # Season peak with the quietest notes dropped.
    _out = []
    for _st in ("AX", "KEMF"):
        _t = tables[_st]
        _keep = archive.select_notes(_t)
        for _min_snr in (5, 8, 11):
            _m = _keep & (_t["snr"] >= _min_snr)
            _out.append(
                {
                    "station": _st,
                    "min SNR (dB)": _min_snr,
                    "frequency_hz": round(
                        archive.histogram_peak(_t["frequency"][_m], archive.FREQ_BINS),
                        2,
                    ),
                    "n_notes": int(_m.sum()),
                }
            )
    mo.ui.table(_out, selection=None)
    return


if __name__ == "__main__":
    app.run()
