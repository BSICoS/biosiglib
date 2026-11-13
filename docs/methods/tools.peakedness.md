---
spec_id: tools.peakedness
title: Measure spectral peakedness
---

# Measure spectral peakedness

## What it does

Computes two percentages around a fixed reference frequency or each spectrum's maximum. PKL measures concentration in a narrow band relative to a wider band; AKL compares the wide-band maximum with the global maximum.

## When to use it

Use it to assess whether a spectrum concentrates power around an expected oscillation or its strongest component. Supply a nonnegative, finite PSD and its increasing frequency grid.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

The default wide band is 0.125 Hz; the narrow band has 40 percent of that width. Both are centered on the reference and include their endpoints. Automatic mode uses the first global maximum, without imposing a physiological frequency interval. Each matrix column is assessed independently.

The concentration measure follows the reference-centered formulation of Kontaxis et al., with the earlier peak-conditioned approach of Lázaro et al. as scientific context. The method applies to spectra independently of signal modality.

## Interpretation and limitations

PKL and AKL range from zero to 100 percent. In automatic mode AKL is always 100 for nonzero spectra, so it provides extra discrimination when a fixed reference is used. Zero spectra and bands without samples return zero for the corresponding measure. A uniform frequency grid is assumed. The band integrals are approximated by equal-width rectangular sums, so the common frequency spacing cancels in PKL. No interpolation is performed. Resolution and bandwidth therefore affect the result. NaN and infinite spectral values are rejected.

<!-- BIOSIGLIB METHOD RESOURCES -->
