# Detector landscape for fin whale 20 Hz pulses

Surveyed 2026-08-29. Constraints assumed: 200 Hz audio, 20 Hz signal,
Apple Silicon, PyTorch preferred, prefer fine-tuning over training fresh.

## Recommendation

**Whale-VAD** as the model, **Schall's DSP detector** as the day-one baseline,
**Madhusudhana's temporal-context trick** as the upgrade once a CNN works.

## Whale-VAD, the pick

`github.com/CMGeldenhuys/Whale-VAD`, GPL-3.0, Zenodo `10.5281/zenodo.17251589`.
`pip install whalevad`, or three lines through `torch.hub`. Dependencies are
`torch`, `torchaudio`, `numpy`. No TensorFlow anywhere. 4 MB checkpoint.

Weights: `github.com/CMGeldenhuys/Whale-VAD/releases/download/v0.1.0/WhaleVAD_ATBFL_3P-c6f6a07a.pt`

```python
classifier, transform = torch.hub.load("CMGeldenhuys/Whale-VAD", 'whalevad', weights='DEFAULT')
audio, sr = ta.load("whale-call.wav")   # sr must be 250
features, _ = transform(audio)
logits, prob, _ = classifier(features)  # frame-level, classes bmabz / d / bp
```

Preprocessing, read from `whalevad/weights.py`:

```
sample_rate=250, n_fft=256, win_length=256, hop_length=5,
norm_features="demean", power=None, complex_repr="trig"
```

Roughly 0.98 Hz bins, 1.024 s window, 20 ms hop, 50 frames/s. `power=None`
keeps phase rather than taking magnitude, which the paper credits for the gain.

**Why it works where Perch cannot.** Architecture is CNN-BiLSTM with a first
layer that convolves over frequency only, commented in source as "act as a
learnable mel". There is no fixed mel filterbank and therefore no low-frequency
floor. Perch's frontend starts at 60 Hz, so a 20 Hz call is below its first band.

**Why the sample rate is close enough to lucky.** Trained at 250 Hz. Our data
is 200 Hz. That is a 1.25x gap, not the 160x gap Perch would have needed.

Performance: F1 0.357 at BioDCASE 2025 (jury award). The follow-up WhaleVAD-BPN
(arXiv 2510.21280) reports F1 0.475 with +9.4% on fin whale calls specifically,
but those improved weights are not released. v0.1.0 is the original.

**Checked 2026-08-30: it emits 7 classes, not 3.** Loaded the released
checkpoint and ran 10 s of noise through it: `logits.shape == (1, 449, 7)`.
So `model.py`'s `_class_mapping = ["bmabz", "d", "bp"]` does **not** describe
the released head, and the README's 3-class description is wrong for these
weights. This is the better outcome: a pooled `bp` would have merged the fin
whale call types, and 7 outputs should keep them separate.

**The label order is undocumented.** Seven is exactly the ATBFL label count
(`bma`, `bmb`, `bmz`, `bp20`, `bp20plus`, `bpd`, `d`), so that is the likely
mapping, but nothing in the repo confirms the order and it should not be
assumed. Resolve it empirically instead: run all 7 channels over a KEMF window
where the 2017 study's archived detections give ground-truth fin whale times,
and see which channel correlates. The first milestone already fetches exactly
that window, so this costs nothing extra.

**Licence note:** GPL-3.0. Fine for this project, which is not billable. Flag it
if anything derived from it ever heads toward client work.

## Baseline to run first

`github.com/elenaschall/Fin-whale-detector`. Pure DSP, no training, no weights.

```python
F20P = {'f0': 15, 'f1': 26, 'nl0': 10, 'nl1': 15, 'nh0': 30, 'nh1': 80}
```

10th-order Butterworth bandpass built per file from that file's own `fs`,
`nfft=fs` so bins are 1 Hz at any rate, Teager-Kaiser energy operator, kurtosis
gates, then joins detections within 2 s. Every band it touches is at or below
80 Hz and nothing is hardcoded to a sample rate, so **it runs on 200 Hz data
unmodified**. No licence file, so default all-rights-reserved. Ask Schall before
shipping anything derived from it.

(`detect_chorus.py` in the same repo is a different tool and reaches 96-100 Hz,
right at our Nyquist. Not the one we want.)

## The upgrade, once a CNN works

Madhusudhana et al. 2021, "Improve automatic detection of animal call sequences
with temporal context", J. R. Soc. Interface 18:20210297. Open access.
Code at `github.com/shyamblast/TemporalContext-2021`, MIT, TensorFlow, no weights.

Demonstrated on fin whale song specifically. Adding an LSTM over the note
sequence on top of a CNN gave 9-17% AUC-PR and 9-18% peak F1 over the CNN alone,
for zero extra labels. Given that fin whale song has a regular IPI by definition,
and that IPI is the thing we are measuring, this is the highest-leverage addition
available. Reported: HARPs at 500 Hz, 4 s segments, 10-54 Hz, 36x21 input,
DenseNet at ~54k parameters, 13,023 annotated notes, AUC-PR 0.82 to 0.95.

## Other obtainable weights

| Model | Access | Notes |
|---|---|---|
| BioDCASE 2026 YOLOv11s baseline | `zenodo.org/records/20281116`, CC-BY-4.0, open, 19.2 MB | Easiest warm start, but Ultralytics is AGPL-3.0 and it is an object detector, so it cannot be fine-tuned inside OpenSoundscape |
| Alksne et al. Faster R-CNN | `10.5281/zenodo.19164291`, **restricted**, HTTP 403 | Best published fin whale numbers, precision 0.87 / recall 0.74. Worth requesting access |
| Google Multispecies Whale Model | `kagglehub`, Apache 2.0 | Has a real `Bp` fin whale class, AUC 0.9909 on held-out. But 24 kHz input, and Google's own card warns metrics degrade off-distribution. Their marine transfer paper: off-the-shelf head scored 0.612 on DCLDE 2026 while embeddings few-shot to 0.954. Use `.embed()`, train your own head, do not trust the shipped logit |
| ANIMAL-SPOT Antarctic blue whale | inside PAMGuard `jpam` test fixtures, GPL-3.0 | `sr 2000, fmin 12, fmax 500`, ResNet-18 TorchScript, ~45 MB. Wrong species, right regime. Apparently the only trained ANIMAL-SPOT checkpoint anywhere |
| Koogu blue whale D-call | same place, `blue_whale_24.kgu` | 250 Hz, 4.5 s, DenseNet. Wrong call type, right regime |

## Perch: settled, and the answer is no

This closes probe 3 without needing to run it.

- Perch 2.0's mel frontend runs 60 Hz to 16 kHz. A 20 Hz call sits below its
  first band. Not a resolution problem, an absence problem.
- Ghani et al. 2023 explicitly **deleted fin whale and northern right whale**
  from their transfer-learning benchmark for being too low frequency.
- Time compression does not rescue it. Tolkova et al. 2026 found an optimum of
  **12x** on a 50-500 Hz signal for about +10 points. 20 Hz would need 50-100x,
  at which point the call becomes shorter than one FFT window.
- `bioacoustics-model-zoo` contains **zero** marine mammal models: 11 bird
  models, YAMNet, and an underwater frog bandpassed to 300-2000 Hz. The
  `local-models.md` note implied otherwise.

Hugging Face has nothing. PAMGuard ships three models, none fin whale. Ketos,
Koogu, INSTINCT, Raven Pro and DeepAcoustics have no fin whale model.

## OpenSoundscape, practical notes

Version 0.13.2 handles `sample_rate=200` natively, no forced resampling, and
`bandpass_range=(10,40)` works. **Must override `window_samples`**: the default
512 is a 2.56 s FFT at 200 Hz. Use 128.

No object-detection API, so the YOLO and Faster R-CNN options above cannot be
fine-tuned inside it. Whale-VAD does not need it, being standalone PyTorch.

Use OpenSoundscape for what it is actually good at here: annotation handling
(`BoxedAnnotations.from_raven_files` then `.clip_labels`), clip datasets, and
training a small custom `nn.Module`.

**Start on `device='cpu'`.** The macOS CI job has been disabled since 2024 over
unresolved MPS OOM errors, and these models are small enough that it costs
nothing.

## Data quantity, if training fresh

Four studies converge on ~1,000-3,000 labelled positives as the working
threshold. The one attempt below it (Roman Ruiz et al. 2023, 1,722 labels) got
26.1% recall. Above it, Roman-Ruiz and Rossi 2026 hit F1 0.98 with a single
conv-ReLU-pool block on 1,232 positives.

Not our binding constraint. ATBFL has ~20,700 free labelled fin whale pulses at
250 Hz, and our own archived detections run to 1.8 million notes.

## The bar

Any new detector has to beat the 2017 paper's own matched filter: **4.8% missed,
1.5% false**. Not "beat nothing".

## The paper-shaped gap

Not one of the twelve BioDCASE 2025 submissions used a foundation model, and the
winner's key move was replacing the fixed mel filterbank with a learnable one.
"Do bird-trained embeddings plus time compression work for 20 Hz fin whale
pulses?" is unanswered, has a public benchmark sitting at F1 0.50, and
BioDCASE 2026 is live.

Worth knowing about. Not this project's scope.

## Confidence

Verified by fetching: Whale-VAD repo, licence, release asset (HTTP 200,
4,255,358 bytes), `hubconf.py`, `weights.py`, `_class_mapping`, PyPI metadata;
the Google model's full metrics table and domain-shift caveat; Madhusudhana's
abstract and repo contents; Schall's `F20P` dict and adaptive filter; Zenodo
access status for BioDCASE (open) and Alksne (restricted).

Relayed but not independently verified: the PAMGuard `jpam` ANIMAL-SPOT and
Koogu checkpoints, Madhusudhana's internal architecture numbers, the Google
model's exact mel floor (two sources conflict, 8 Hz vs 20 Hz), and the
Madhusudhana dataset DOI (Zenodo rate-limited the search).
