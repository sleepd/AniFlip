bl_info = {
    "name": "AniFlip",
    "author": "Qiao Xu",
    "version": (0, 1, 0),
    "blender": (4, 5, 0),
    "category": "Animation",
    "description": "Mirror keyframes and apply cycle offsets",
}

import bpy
from . import operators, ui


def _cycle_frames_property():
    return bpy.props.IntProperty(
        name="Cycle Frames",
        description="Total length (frames) of the current cycle",
        default=30,
        min=1,
    )


def _direction_property():
    return bpy.props.EnumProperty(
        name="Direction",
        description="Mirror from right to left or left to right",
        items=(
            ("RL", "R -> L", "Flip from right to left"),
            ("LR", "L -> R", "Flip from left to right"),
        ),
        default="RL",
    )


classes = (
    operators.ANIFLIP_OT_close_cycle,
    operators.ANIFLIP_OT_cycle_mirror,
    ui.ANIFLIP_PT_main_panel,
)


def register():
    print("AniFlip: registering classes (4.5)")
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.aniflip_cycle_frames = _cycle_frames_property()
    bpy.types.Scene.aniflip_direction = _direction_property()


def unregister():
    print("AniFlip: unregistering classes (4.5)")
    del bpy.types.Scene.aniflip_cycle_frames
    del bpy.types.Scene.aniflip_direction
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
