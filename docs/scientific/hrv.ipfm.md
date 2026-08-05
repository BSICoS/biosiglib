---
spec_id: hrv.ipfm
title: IPFM heart-timing reconstruction and TVIPFM modulation
status: draft
---

# IPFM heart-timing reconstruction and TVIPFM modulation

## Purpose

The heart-timing approach reconstructs a continuous instantaneous-rate signal from discrete beat or pulse occurrence times. Its optional TVIPFM output estimates autonomic modulation while compensating for a slowly changing mean heart rate.

## Scientific rationale

Mateo and Laguna formulate heart timing as cumulative event count versus time. Differentiating a smooth interpolation of that count produces instantaneous rate in hertz. Their work specifically studies fourteenth-order spline interpolation, and later work applies the same order after removing incorrect event values. This supports the default spline order, but it does not make every edge-stabilization constant a physiological parameter.

The virtual events added outside the observed sequence reduce boundary instability. Biosiglib fixes ten virtual events per side and estimates their spacing from at most eight nearby intervals because those values preserve the mature Biosigmat behavior. The publications do not prescribe these exact `10/8` values, so they are documented as empirical numerical constants rather than scientifically validated thresholds.

## TVIPFM interpretation

Under a time-varying mean heart rate, the conventional IPFM relationship causes the apparent variability amplitude to scale with that mean rate. TVIPFM Approach A estimates the slowly varying mean instantaneous rate, subtracts it from the instantaneous rate, and divides the residual by the mean. The resulting dimensionless signal represents modulation relative to the time-varying baseline rather than an unnormalized high-pass residual.

Bailón et al. validate this correction during exercise and use a 0.03 Hz separation for the time-varying mean rate. Sörnmo, Bailón, and Laguna later derive and review the model in broader time-varying and confounded conditions. Those publications support the model semantics and cutoff, but they do not define Biosigmat's exact fourth-order Butterworth implementation or its forward-backward edge padding.

## Assumptions and limitations

Event times must already be finite, correctly ordered, and physiologically meaningful. High-order splines can overshoot for pathological interval patterns even without extrapolation; non-positive reconstructed rates are therefore rejected rather than clipped. Virtual events stabilize the spline near the boundaries but do not justify evaluating outside the observed time interval.

The modulating signal assumes a positive, slowly varying mean rate and enough uniformly sampled data to support zero-phase filtering. It should be interpreted as a model-based autonomic modulation estimate, not as a direct physiological measurement or a generic detrended HRV series.

## References

The heart-timing reconstruction and order-14 evidence come from Mateo and Laguna (2000, 2003). The TVIPFM correction and exercise validation come from Bailón et al. (2011), with later derivation and review context from Sörnmo, Bailón, and Laguna (2024).

## Specification

The normative contract is the generated [`hrv.ipfm` specification](../generated/specifications/hrv.ipfm.md).
