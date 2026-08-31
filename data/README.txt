Gitignored. Data retrieved from elsewhere. Two kinds live here.

Raw waveform data retrieved from FDSN web services.

  Nothing here is irreplaceable. Every retrieval writes a manifest to
  manifests/, which is committed, recording network, station, channel, time
  window, response epoch, sample rate, code version and retrieval timestamp.
  Any file in this directory can be reconstructed from that manifest.

fin-call-patterns/, the 2017 study's archived per-note detections.

  A clone of github.com/michellejw/fin-call-patterns pinned to the commit
  recorded in manifests/ground-truth-fin-call-patterns.json, which also
  carries sha256 for each of the 23 station-season HDF5 files. That upstream
  has no licence and no DOI, so the pin and the checksums are what make it
  reproducible. Restore with:

    git clone https://github.com/michellejw/fin-call-patterns.git \
      data/fin-call-patterns
    git -C data/fin-call-patterns checkout <commit from the manifest>

  Roughly 1.1 GB on disk. Only DETECTION_DATA/ is used.

Delete either freely.
