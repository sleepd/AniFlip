# AniFlip

Blender插件，用于将一侧姿态关键帧镜像到另一侧，并按循环长度的一半做偏移（例：48 帧走路，L 的第 1 帧映射到 R 的第 25 帧）。UI 在 3D 视图的 N 面板，仅在 Pose Mode 可见。

## 安装
1. 从 GitHub Release 下载 `.zip`。
2. Blender 中：Edit → Preferences → Add-ons → Install… 选择该 `.zip`，启用 “AniFlip”。

## 使用
1. 进入 Pose Mode，打开 3D 视图，按 `N` 打开侧栏，切到 `AniFlip` 标签。
2. 设置：
   - `Cycle Frames`：循环总帧数（建议偶数，如 48）。
   - `Direction`：`R -> L` 或 `L -> R`。
3. 点击 `Cycle Mirror`，会将源侧的关键帧镜像到另一侧，并按半周期偏移到对应帧。

## 注意
- 骨骼命名需遵循 `.L` / `.R` 后缀成对。
- 当前对象必须是骨架、Pose Mode 且有 Action；如果源侧没有关键帧会直接中止并提示。
