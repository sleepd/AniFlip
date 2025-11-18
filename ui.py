import bpy


class ANIFLIP_PT_main_panel(bpy.types.Panel):
    """Basic 3D View N-panel for AniFlip (Blender 4.5)"""
    bl_label = "AniFlip"
    bl_idname = "VIEW3D_PT_aniflip"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AniFlip"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj and obj.type == "ARMATURE" and obj.mode == "POSE"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "aniflip_cycle_frames")
        layout.prop(scene, "aniflip_direction", expand=True)

        layout.separator()
        layout.operator("aniflip.close_cycle", text="Close Cycle")
        layout.operator("aniflip.cycle_mirror", text="Cycle Mirror")
