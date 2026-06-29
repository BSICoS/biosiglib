---
spec_id: ecg.sloperange
title: Slope-range ECG-derived respiration
status: draft
---

# Slope-range ECG-derived respiration

## Purpose

Slope-range ECG-derived respiration estimates a beat-to-beat respiratory modulation signal from ECG morphology. It is useful when a respiratory belt or airflow signal is unavailable but reliable ECG R-wave timing and derivative morphology are available.

## Scientific rationale

Respiration changes the position of the heart and the electrical axis seen by a single ECG lead. These changes modulate QRS morphology, including the steepness of the ECG derivative around each R wave. The slope-range method uses that morphology modulation as a surrogate respiratory signal.

## Method summary

For each detected R wave, the method inspects short derivative-ECG windows around the beat. It compares the strongest local upslope with the strongest local downslope and stores their difference as the EDR amplitude for that beat. Beats whose analysis windows fall outside the signal keep their alignment but receive missing-value markers.

## Key assumptions

The method assumes R-wave times are reliable, the derivative ECG emphasizes QRS slope information, and respiratory motion meaningfully modulates the observed ECG morphology. It is intended as an EDR amplitude series, not as a direct measurement in physical respiratory units.

## Interpretation and limitations

Larger EDR values indicate stronger local slope-range modulation around a beat. Interpretation should focus on trends or derived respiratory rate estimates after suitable post-processing. The method may be unreliable when R-wave detections are wrong, QRS morphology is unstable for non-respiratory reasons, ECG noise is high, or boundary beats lack enough neighboring samples.

## References

* Kontaxis et al. 2020, [doi:10.1109/TBME.2019.2923587](https://doi.org/10.1109/TBME.2019.2923587), provides the main method provenance for the slope-range EDR contract.
* Varon et al. 2020, [doi:10.1038/s41598-020-62624-5](https://doi.org/10.1038/s41598-020-62624-5), compares ECG-derived respiration approaches in ambulatory single-lead ECG.

## Specification

The normative contract is the generated [`ecg.sloperange` specification](../generated/specifications/ecg.sloperange.md).
