# Probe 7: what explains the KEMF frequency offset?

2026-10-17. Answer: not fully worked out. Sensor type, sample rate, depth and
geography are ruled out. Background noise explains part of it, about 0.2 Hz of
0.7 Hz. The remaining 0.5 Hz is unexplained.

## Why this was asked

Probe 6 found that in 2011-2012 KEMF reads about 0.8 Hz higher than Axial for
the same whales in the same season, while IPI agrees. That offset is more than
half of the whole decadal frequency change, so it matters for any KEMF
comparison against the published trend. Probe 6 listed candidate explanations
without testing them: sensor type, depth, propagation path, and a noise floor
that shifts an amplitude-weighted centroid.

Seven stations recorded in 2011-2012, with different sensors, depths and
sample rates. If the offset follows one of those, it should show up across
them.

## What was done

Ran the probe 6 recipe (singlet A notes, the house filters, 1D histogram peak)
on all seven 2011-2012 files in `DETECTION_DATA/`. Station details are from the
paper's Table 1, via `notes/literature/2017-paper-data-section.md`. Then split
each station's notes by SNR to test the noise explanation.

Code: `notebooks/02_station_comparison.py`. Table: `results/stations_2011_2012.csv`.

## Evidence

### The seven stations

| Station | Sensor | Depth | Rate | Frequency | IPI | Notes |
|---|---|---|---|---|---|---|
| AX | hydrophone | 1550 m | 100 Hz | 18.45 Hz | 28.75 s | 36,384 |
| KEMF | seismometer | 2205 m | 100 Hz | **19.15 Hz** | 28.25 s | 15,268 |
| J63A | seismometer | 2880 m | 50 Hz | 18.35 Hz | 28.75 s | 48,855 |
| J23A | seismometer | 2660 m | 50 Hz | 18.45 Hz | 29.25 s | 40,412 |
| J06A | seismometer | 3220 m | 50 Hz | 18.35 Hz | 33.25 s | 151,338 |
| G30A | seismometer | 3120 m | 50 Hz | 18.15 Hz | 32.75 s | 77,505 |
| G03A | seismometer | 4110 m | 50 Hz | 18.45 Hz | 33.75 s | 43,566 |

Six stations agree within 0.3 Hz (18.15 to 18.45). KEMF is the only outlier.
With these 1D peaks the KEMF-Axial gap is 0.70 Hz. The 0.80 Hz in probe 6
comes from the archived 2D summary (19.2 against 18.4).

### Ruled out

- **Sensor type.** KEMF is a seismometer, but so are the five Cascadia
  stations, and they agree with the Axial hydrophone. Seismometer against
  hydrophone is not the difference.
- **Sample rate.** KEMF and Axial are both 100 Hz, and they are the pair that
  disagree.
- **Depth.** KEMF (2205 m) sits between Axial (1550 m) and the Cascadia
  stations (2660-4110 m), which all read lower. No depth ordering puts KEMF
  alone at the top.
- **Different whales, or geography.** J63A is 73 km from KEMF, closer than
  Axial (232 km), and reads 18.35 Hz, in line with everything except KEMF.
- **Instrument response.** Already ruled out by probe 5: flat to 0.20 dB
  across 15-35 Hz.

### Partly explained: noise

Frequency peak per SNR bin, singlet A notes:

| Station | 5-8 dB | 8-11 dB | 11-15 dB | 15-20 dB | 20+ dB |
|---|---|---|---|---|---|
| AX | 18.65 | 18.45 | 18.45 | 18.45 | 18.55 |
| KEMF | **21.95** | 19.25 | 18.85 | 19.15 | 18.65 |

Axial barely moves with SNR. KEMF's quietest notes, 47% of its total, peak at
21.95 Hz, right at the A/B boundary. That fits the noise-floor explanation: in
a quiet note, background noise carries more of the weighted centroid, and at
KEMF that pulls it upward.

Dropping the quietest notes moves KEMF from 19.15 to 18.95 Hz. Axial stays at
18.45 Hz at every threshold (SNR >= 8 and >= 11 dB). The gap shrinks from
0.70 to 0.50 Hz and stops shrinking: the 11-15 and 15-20 dB bins still read
0.4-0.7 Hz high. The 20+ dB bin reads only 0.1 Hz high, but holds 399 notes,
too few to lean on.

## Answer

I could not fully work out what explains the offset. What is settled:

- It is specific to KEMF, not to seismometers, 100 Hz sampling, depth, or that
  part of the ridge.
- Background noise accounts for about 0.2 Hz of it. The quietest KEMF notes are
  biased high, and the house recipe's SNR > 5 dB filter lets them in.
- About 0.5 Hz remains in loud, clean notes, where noise should not matter.

## Caveats

- The five Cascadia stations sample at 50 Hz. The paper excluded them from
  frequency analysis because the anti-alias cutoff at 23.5 Hz trims the note
  and skews the centroid low. Their agreement with Axial could be partly
  coincidence. The only same-rate comparison is Axial against KEMF.
- All of this uses 1D histogram peaks, not the archive's 2D extraction.

## Not explained, worth trying next

- What is left of the 0.5 Hz: something about the KEMF site or how the sensor
  couples to the seafloor (it is a corehole seismometer, probe 5), or the
  propagation path into the Endeavour axial valley. None of these can be tested
  from the per-note files alone. They would need the waveforms.
- Whether the noise effect is the same in 2012-2013. That season has no
  Axial singlet to compare against.

## Also noticed, not pursued

IPI splits into two groups that frequency does not: about 28-29 s at AX,
KEMF, J63A and J23A, and about 33 s at J06A, G30A and G03A. The split falls
between J23A (44.84N) and J06A (43.25N), so it follows latitude. The archived
2D summary shows two singlet clusters, near 28.5 and 32.5 s, at J23A and J06A,
so both may be present in the middle of the array. Not tested here.
