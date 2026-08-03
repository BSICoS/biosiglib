---
spec_id: hrv.removefp
title: False-positive event removal
status: draft
---

# False-positive event removal

## Purpose

False-positive event removal cleans a beat- or pulse-detection time series before interval analysis or missing-event reconstruction. It is intended to remove detections that occur implausibly soon after a preceding event relative to the local timing pattern.

## Scientific rationale

An extra detection creates an abnormally short event-to-event interval. Comparing each interval with a median-filtered local baseline provides a robust deterministic way to identify these short intervals without using the event-signal morphology.

## Method summary

The method derives all successive intervals from the original event series, obtains an adaptive local baseline, and flags sufficiently short intervals. It then removes the later event of each flagged pair simultaneously. The baseline is not recomputed after removal, so the operation remains a transparent single preprocessing pass.

## Key assumptions

The event series must already be finite and correctly ordered. The method assumes an abnormally short interval is evidence of an extra detection and that removing the later event is the intended deterministic choice. The fixed threshold settings are empirical algorithm constants inherited from prior Biosigmat use.

## Interpretation and limitations

The result should be inspected as a cleaned event sequence, not interpreted as a clinical classification. Timestamps alone may not distinguish an extra detection from a nearby true event, so the rule can retain a false detection and remove a true event in ambiguous local patterns. Signal morphology or detector-quality information may support more advanced methods, but those inputs are outside this contract.

## References

No primary clinical-validation reference is claimed for the empirical threshold constants in this initial contract.

## Specification

The normative contract is the generated [`hrv.removefp` specification](../generated/specifications/hrv.removefp.md).
