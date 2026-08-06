---
spec_id: hrv.osp
title: Respiratory decomposition by orthogonal subspace projection
status: draft
---

# Respiratory decomposition by orthogonal subspace projection

## Purpose

Respiration changes heart rate through respiratory sinus arrhythmia and other cardiorespiratory interactions. Those changes can move across conventional HRV frequency bands when breathing rate varies, which complicates interpreting spectral powers as fixed autonomic components. Orthogonal subspace projection (OSP) separates the uniformly sampled HRV modulation into a part that can be represented by respiration and delayed copies of respiration, and a residual part outside that linear subspace.

## Scientific rationale

Varon and colleagues use OSP to quantify and remove linear respiratory influences from HRV. The respiration-related component is obtained by projecting HRV onto a basis constructed from respiration, while the residual contains the dynamics not represented by that basis. Their studies support this decomposition and show why accounting for respiration can improve HRV interpretation under changing respiratory patterns.

The residual is not a respiration-free physiological signal in an absolute sense. OSP removes only the component that is linearly represented by the chosen respiratory subspace. Nonlinear respiratory effects, measurement noise, unrelated autonomic modulation, and errors in the respiratory signal can remain.

## Adaptive respiratory subspace

Biosiglib preserves the Biosigmat choice of an adaptive model order spanning approximately two cycles of the selected respiratory frequency. This connects faster breathing to a shorter delayed basis and slower breathing to a longer one. The resulting order also determines the samples lost while the delayed vectors become fully defined, so the decomposition starts later than the original synchronized signals.

The preceding dominant-frequency selection is deliberately documented as an inherited empirical heuristic. Its 90% occupied-power band, peak-count-dependent choice, and minimum-frequency floor are compatibility decisions, not mathematical requirements of OSP and not optimal values established by the cited publications. Implementations should preserve them for reproducibility without assigning them broader physiological authority.

## Numerical reproducibility

The delayed respiration columns can be dependent or nearly dependent. Such subspaces remain meaningful, but their Gram matrix requires a truncated pseudoinverse. Biosiglib fixes the binary64 threshold used by the mature MATLAB calculation so MATLAB and Python retain the same singular directions instead of relying on different library defaults.

This internal rank decision is separate from the tolerances used to compare returned components. Forming the Gram matrix squares the subspace condition number, so the residual orthogonality check is intentionally less strict than direct component and reconstruction comparisons.

## Assumptions and limitations

The HRV modulation and respiration must already share a uniform sampling grid and time alignment. Biosiglib does not define how respiration is measured, preprocessed, or converted into a PSD within this contract. Poor synchronization, artifacts, weak respiratory information, or a PSD that does not represent the analyzed segment can make the mathematical decomposition physiologically misleading even when it is numerically conformant.

The respiration-related output describes association with the selected linear subspace, not causal influence. Likewise, the residual should not be interpreted as a pure sympathetic component or as proof that respiratory effects have been completely removed.

## References

The delayed-respiration OSP interpretation and its use during emotional stress are described by Varon et al. (2017). The broader HRV analysis and validation after removing respiratory influences are presented by Varon et al. (2019).

## Specification

The normative contract is the generated [`hrv.osp` specification](../generated/specifications/hrv.osp.md).
