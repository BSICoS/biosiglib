---
spec_id: hrv.ipfm
title: IPFM heart-timing reconstruction and TVIPFM modulation
---

# IPFM heart-timing reconstruction and TVIPFM modulation

## What it does

This method reconstructs uniformly sampled instantaneous heart rate from discrete beat or pulse occurrence times. It can also estimate dimensionless TVIPFM modulation relative to a slowly changing mean rate.

## When to use it

Use it when an interval sequence must be converted into a uniformly sampled heart-rate or modulation signal for spectral or multivariate analysis.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

A high-order B-spline interpolates cumulative event count after adding virtual boundary events for numerical stability. Its derivative gives instantaneous rate on the requested uniform grid. When modulation is requested, a zero-phase low-pass estimate of mean rate is removed and used to normalize the residual.

The default spline order and boundary extension are empirical numerical choices. The 0.03 Hz separation used by TVIPFM is supported by the cited method literature.

## Interpretation and limitations

Event times must already be ordered, finite, and physiologically meaningful. High-order interpolation can overshoot on pathological timing patterns. The modulation output is model-based and should not be interpreted as a direct autonomic measurement.

<!-- BIOSIGLIB METHOD RESOURCES -->
