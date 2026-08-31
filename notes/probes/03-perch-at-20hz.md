# Probe 3: does Perch work at 20 Hz?

2026-08-29. Answer: no. Closed from the literature without running it.

## Question

Perch is fixed at 32 kHz. Our data is 200 Hz and the signal is at 20 Hz. Does
the time-compression trick (speed the audio up so 20 Hz lands in Perch's
sensitive band) rescue it, or is Perch simply the wrong tool?

## Answer

Wrong tool. Four independent lines, none of which required running anything.

1. Perch 2.0's mel frontend runs 60 Hz to 16 kHz. A 20 Hz call sits below its
   first band. This is an absence, not a resolution shortfall.
2. Ghani et al. 2023 explicitly removed fin whale and northern right whale from
   their transfer-learning benchmark for being too low frequency. Someone
   already tried and gave up on exactly this.
3. Time compression has a measured optimum and it is far below what we need.
   Tolkova et al. 2026 found 12x optimal on a 50-500 Hz signal for about
   +10 points. 20 Hz needs 50-100x, at which point the call becomes shorter
   than one FFT window.
4. `bioacoustics-model-zoo`, the recommended TensorFlow-free Perch path, has
   zero marine mammal models. Eleven bird models, YAMNet, and an underwater
   frog bandpassed to 300-2000 Hz.

## Consequence

Perch leaves the project entirely rather than staying as an optional spike.
The project rename from `fin-whale-perch` is retroactively correct.

Also worth noting: not one of the twelve BioDCASE 2025 submissions used a
foundation model, and the winning entry's key move was replacing the fixed mel
filterbank with a learnable one. The replacement model we picked, Whale-VAD,
is that winning entry.

## Where this leaves the detector

Whale-VAD. PyTorch, 250 Hz training rate against our 200 Hz, dedicated fin
whale class, learnable frequency frontend and therefore no mel floor.
See `../literature/detector-landscape.md`.
