# Probe 1: is the 2003-2013 data re-downloadable?

2026-08-29. Answer: yes.

## Question

Validation depends on re-running the new detector on the data the 2017 study
analysed. That needs the old audio. Is it public, or does it survive only on
archived drives?

## Method

FDSN station web service, bounding box from the paper (40-48 N, 130-125 W),
2003-01-01 to 2013-12-31, station and channel level.

```
https://service.iris.edu/fdsnws/station/1/query
  ?minlat=40&maxlat=48&minlon=-130&maxlon=-125
  &starttime=2003-01-01&endtime=2013-12-31
  &level=station&format=text
```

## Result

391 stations in the box for that era.

| Network | Stations | Era |
|---|---|---|
| 7D | 106 | 2011-2014 |
| SY | 90 | synthetic, exclude |
| X6 | 73 | 2012 |
| X9 | 45 | 2012-2013 |
| Z5 | 39 | 2013-2014 |
| YN | 35 | 2009 |
| NV | 3 | 2009- (Ocean Networks Canada) |

Hydrophone and pressure channels (`?DH`) present:

| Network | Channel | Rate | Count |
|---|---|---|---|
| X6 | EDH | 200 Hz | 73 |
| YN | EDH | 200 Hz | 35 |
| Z5 | HDH | 100 Hz | 39 |
| X9 | HDH | 100 Hz | 20 |
| 7D | HDH | 125 Hz | 19 |
| 7D | BDH | 40/50 Hz | 80 |
| various | LDH | 1 Hz | too coarse |

## What matters

X6 and YN carry hydrophone channels at exactly 200 Hz, the same rate as the
OOI low-frequency hydrophones. Same rate across both eras means one detector
front end and no resampling difference. This is what makes "one pipeline,
both eras" cheap rather than expensive.

## Caveats

- Hydrophone coverage in the box spans 2009-2014 only. Nothing 2003-2008.
  Fine for validation, which needs an overlapping year or two, but the
  old-method comparison can only anchor in the back half of the record.
- The bounding box returns everything in the region, not the study's stations.
  Validating against published numbers requires those specific stations.
  Temporary network codes (X6, X9, YN, Z5) are reused across unrelated
  campaigns, so the code alone does not identify a deployment.
- SY is the synthetic seismogram network. Not real data.

## Gotcha

`service.iris.edu` now 307-redirects to `service.earthscope.org`. Without
`curl -L` you get an empty body, HTTP 307, and no error message.
