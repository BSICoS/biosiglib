---
spec_id: hrv.fdmetrics
title: Frequency-domain HRV metrics
---

# Frequency-domain HRV metrics

## Purpose

Frequency-domain HRV analysis summarizes how the variability of heart timing is distributed over frequency. The conventional form reports low-frequency (LF) and high-frequency (HF) power and two normalized ratios. The respiration-separated form instead combines spectra obtained after orthogonal subspace projection (OSP) to distinguish power linearly related to respiration from respiration-unrelated LF power.

## Scientific rationale

The conventional LF and HF bands provide a widely used descriptive organization of HRV spectra. They are useful for reproducible comparisons, but the physiological interpretation of each band is not unique: respiration, autonomic regulation, baroreflex dynamics, posture, activity, and analysis conditions can all influence the measured powers. In particular, respiration can move across nominal bands as breathing frequency changes.

OSP offers a complementary description. After HRV modulation has been separated into respiration-related and residual components, their spectra can support an index based on respiration-unrelated LF power relative to the combined related and unrelated power. The resulting normalization is bounded and remains defined when related power is exactly zero, but it still reflects the quality and assumptions of the preceding decomposition.

## Frequency-grid interpretation

Biosiglib treats the supplied frequency grid and PSD samples as the observations. Band-edge samples are selected from that grid and integrated directly rather than estimated by interpolation. This makes the calculation transparent and preserves the mature implementation, while also making results sensitive to spectral resolution and irregular spacing near 0.04, 0.15, and 0.4 Hz.

Partial nominal coverage is not automatically a failure. For example, a spectrum ending below 0.4 Hz can still provide an HF estimate over the represented range. Such a value should be reported with awareness that it does not cover the full conventional HF interval.

## Diagnostics and compatibility limits

The VLF diagnostic flags a spectrum whose integrated power below the LF boundary is large relative to the remaining represented power. It is a quality signal only and does not alter otherwise valid metrics. When more than one spectrum triggers the same condition, a single warning identifies all affected spectra so callers receive complete information without repeated messages.

Exact zero required LF or HF power is handled separately because normalized ratios would be undefined or uninformative. This condition invalidates the selected mode's result and is reported through its own aggregated warning. A VLF warning and a zero-power warning may therefore coexist.

The two upper-power rejections retained for the OSP-separated mode are empirical compatibility limits tied to dimensionless modulation spectra. They should not be generalized to arbitrary PSD units. For the same reason, the former large-power rejection in the conventional mode is removed: conventional spectra may legitimately use different units and scales.

## Assumptions and limitations

The input PSD must already be a scientifically appropriate estimate for the signal and interval under study. Biosiglib does not prescribe detrending, windowing, spectral estimation, normalization, record length, stationarity, or artifact correction in this contract. These choices can dominate the interpretation even when the final integration is numerically conformant.

The respiration-separated metrics additionally assume that the supplied spectra correspond to the dimensionless related and unrelated modulation components from a suitable OSP analysis. They quantify association with that model, not causal respiratory influence and not a pure sympathetic or parasympathetic component.

## References

The conventional band terminology and normalized powers follow the Task Force recommendations (1996). Varon et al. (2019) describe HRV analysis after removing linear respiratory influences with OSP. Liu et al. (2019) present the improved time-variant cardiorespiratory relation and robust normalized index used by the separated mode.

## Specification

The normative contract is the generated [`hrv.fdmetrics` specification](../generated/specifications/hrv.fdmetrics.md).
