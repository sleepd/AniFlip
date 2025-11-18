# AniFlip

Blender Addon for mirroring pose keyframes with a half-cycle offset (e.g., a 48f walk: frame 1 on L maps to frame 25 on R). UI lives in the 3D Viewport sidebar (N‑panel) and is visible only in Pose Mode.

[中文版说明](./README_zh.md)

## Installation
1. Download the release `.zip` from the GitHub repo.
2. In Blender: Edit → Preferences → Add-ons → Install…, pick the `.zip`, then enable “AniFlip”.

## Usage
1. Enter Pose Mode, open 3D Viewport, press `N`, switch to the `AniFlip` tab.
2. Set parameters:
   - `Cycle Frames`: total cycle length (prefer even numbers like 48).
   - `Direction`: `R -> L` or `L -> R`.
3. Click `Cycle Mirror` to mirror keys to the opposite side with a half-cycle offset.

## Notes
- Bone names must use `.L` / `.R` suffix pairs.
- The active object must be an armature in Pose Mode with an Action; if no source-side keys are found, the operator stops with a warning.
