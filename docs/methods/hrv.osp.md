---
spec_id: hrv.osp
title: Respiratory decomposition by orthogonal subspace projection
---

# Respiratory decomposition by orthogonal subspace projection

## What it does

Orthogonal subspace projection separates uniformly sampled HRV modulation into a component represented by respiration and delayed copies of respiration, plus a residual outside that linear subspace.

## When to use it

Use it to quantify or remove linear respiratory association when HRV modulation and respiration are synchronized on the same uniform sampling grid.

<!-- BIOSIGLIB METHOD INTERFACE -->

## How it works

A dominant respiratory frequency sets an adaptive delayed-respiration model spanning approximately two cycles. HRV is projected onto that subspace, and the residual is obtained by subtraction. The dominant-frequency selection and minimum-frequency floor are empirical algorithm choices.

## Interpretation and limitations

The related component measures linear association, not causal respiratory influence. Nonlinear effects, synchronization errors, artifacts, poor respiratory measurements, and unrelated dynamics can remain in the residual.

<!-- BIOSIGLIB METHOD RESOURCES -->
