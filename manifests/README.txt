Committed. Provenance records, one JSON per retrieval. This directory is
what makes data/ disposable.

Two kinds, distinguished by the "kind" field:

  fdsn-pull        network, station, channel, time window, response epoch,
                   sample rate, code version and retrieval timestamp.

  external-archive an upstream repository or dataset, pinned by commit or
                   version, with a sha256 per file so drift is detectable.
