---
spec_id: ppg.pulsenv
title: Estimate PPG pulse envelopes
---

# Estimate PPG pulse envelopes

## What it does

Joins basal amplitudes to form the lower envelope and apex amplitudes to form the upper envelope. Both curves share the PPG sample grid.

## When to use it

Pass pulse detection times to delineate both fiducials with `pulsedel`, or supply the apex and basal times you already have. Supply the sampling frequency in Hz and express all times in seconds from the first PPG sample.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

Each refined fiducial selects the amplitude and time of its nearest PPG sample. PCHIP interpolates between those anchors. Set `max_gap` in seconds to split each curve wherever successive valid fiducials of its own type reach that separation. Each segment needs at least two distinct sampled anchors.

## Interpretation and limitations

The envelopes can bridge missing PPG samples when there are sufficiently close anchors on either side. Outside supported segments the corresponding curve is NaN. The two curves can begin and end at different samples. They are fitted independently and may cross.

<!-- BIOSIGLIB METHOD RESOURCES -->
