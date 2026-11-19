---
spec_id: ppg.pulsedel
title: Delineate PPG pulse fiducials
---

# Delineate PPG pulse fiducials

## What it does

Locates the apex, basal point and mid-amplitude point for each supplied detection. An aligned derivative also allows the rising-edge onset to be located.

## When to use it

Use detection times on the rising edge from `pulsedet` or another detector. The mid-amplitude time is useful for pulse interval measurements. If onset timing is needed, supply a derivative on the same time grid as the PPG and compensate its filter delay before delineation.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The apex and basal point are extrema on opposite sides of the detection. The midpoint uses the level halfway between their sampled amplitudes. The onset uses the supplied derivative and a threshold of five percent of the maximum upslope for that pulse.

## Interpretation and limitations

All times are in seconds. Each result corresponds to the detection at the same position, even when times are repeated, unsorted or missing. Searches stop at missing PPG samples. Derivative gaps affect only the onset.

Python always returns four arrays. Omitting the derivative silently fills the onset array with one NaN per detection. MATLAB accepts calls for up to three outputs without the derivative and raises an error when the fourth output is requested without it.

<!-- BIOSIGLIB METHOD RESOURCES -->
