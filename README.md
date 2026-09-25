# Football Shorts Generator

Turn one full football match into one vertical highlight Short.

Inspired by the pipeline architecture of Anil-matcha/AI-Youtube-Shorts-Generator, but redesigned for football match events instead of transcript-based talking-head highlights.

## MVP pipeline

```
FULL MATCH
  -> candidate detection
  -> football event scoring
  -> duplicate/replay collapse
  -> chronological selection
  -> FFmpeg cuts
  -> vertical 9:16 reframe
  -> concatenate
  -> one short.mp4
```

MVP input: a local match video you own or are licensed to process.

MVP output:
- one 9:16 MP4
- target duration 60-90 seconds
- original match audio
- highlights kept in match chronology
- events.json with detected/selected events

## Event priority

1. Goals
2. Penalties and red cards
3. Big saves / clear chances
4. Woodwork
5. Other high-intensity moments

## Status

Initial project skeleton. The first detector uses audio-energy peaks as candidate generation. Football-specific visual/event verification is the next layer.
