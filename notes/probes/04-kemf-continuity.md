# Probe 4: is there a station with no gap?

2026-08-30. Answer: yes, and it is one of the paper's own three trend stations.

## Why this was asked

MW on `index.md`: "are we sure there is no nearby OOI data we could use that
does cover the gap? It doesn't need to be at axial."

The Axial plan carried a 2013-2015 gap and, per MW, the old Axial audio
probably arrived on a hard drive and is likely gone.

## What the old code revealed

`DET_CODE/IRISdownload_mseed.m` in `michellejw/fin-call-patterns` is a
MATLAB script that pulls from the IRIS timeseries web service. Verbatim:

```matlab
network = 'NV'   % 7D is CIET network, NV is neptune canada/ONC
stations{1} = 'KEMF';
channels{1} = 'EHZ';
startdate = datenum('01-Oct-2012','dd-mmm-yyyy');
enddate   = datenum('01-Apr-2013','dd-mmm-yyyy');
```

So the paper's missing FDSN codes are recoverable from the code even though
they never appear in the text: **KEMF is network NV, channel EHZ**, and 7D is
the Cascadia Initiative. KEMF data was downloaded from IRIS, not handed over
on a drive. MW's hard-drive memory is probably right for Axial and KENE and
wrong for KEMF.

## The finding

`KEMF` EHZ channel epochs from the FDSN station service:

| Rate | From | To |
|---|---|---|
| 100 Hz | 2010-09-30 | 2013-03-01 |
| 200 Hz | 2013-03-01 | 2014-05-19 |
| 200 Hz | 2014-05-19 | **open, still recording** |

**KEMF EHZ has run continuously from September 2010 to the present.**
No gap. Same station, same channel, same instrument type, cabled power and
timing throughout.

Station is NV.KEMF, Main Endeavour Field, 47.9496N 129.0987W, 2190 m.

## Why this beats Axial

| | Axial (NeMO) | KEMF (ONC) |
|---|---|---|
| Gap | 2013 to 2015 | none |
| Old audio | probably lost, hard drive | on IRIS, code proves it was fetched there |
| Instrument change across era | OBH then OOI hydrophone | same sensor throughout |
| In the paper's trend fit | yes | yes |
| Sample rate | 100 then 200 Hz | 100 then 200 Hz, changed 2013-03-01 |
| Sensor type | hydrophone | short-period vertical seismometer |

The rate change is trivial: decimate 200 to 100 Hz. The band of interest,
15-35 Hz, sits far below both Nyquists.

## Honest caveats

- KEMF is a seismometer, not a hydrophone. The 2017 paper analysed frequency
  on seismometers anyway (both KENE and KEMF are in the Fig 7 fit), so this is
  consistent with the published method rather than a departure from it.
- ~~The 2013-03-01 rate change may carry a response change in 15-35 Hz.~~
  **Checked 2026-08-30 and it does not.** Both epochs tilt +0.20 dB across
  the band and differ from each other by 0.004 dB, on the same GeoSENSE BH-1
  corehole sensor throughout. See `05-instrument-response.md`. The switch
  introduces no residual risk.
- Axial remains the better *hydrophone* story if the audio can be recovered
  from PMEL or NCEI. Not needed for a first result.
- Other Endeavour stations exist for spatial redundancy: NCHR from 2010-10-03,
  ENWF and KEMO from 2016, ENHR from 2018, ENEF from 2020.

## Consequence

The structural limitation recorded in `index.md` ("no temporal overlap, so the
instrument transition cannot be validated") **dissolves at KEMF**. There is no
instrument transition to validate. The old-versus-new comparison becomes purely
a detector comparison on identical hardware, which is exactly the clean
experiment the validation phase wanted and could not have at Axial.
