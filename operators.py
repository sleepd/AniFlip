import bpy
import re
from math import floor


def _mirror_name(name: str):
    if name.endswith(".L"):
        return name[:-2] + ".R"
    if name.endswith(".R"):
        return name[:-2] + ".L"
    return None


def _iter_action_fcurves(action):
    """Yield all F-Curves from an action using Blender 5.0's layered system."""
    if not action:
        return
    for layer in action.layers:
        for strip in layer.strips:
            if strip.type != "KEYFRAME":
                continue
            for bag in strip.channelbags:
                for fc in bag.fcurves:
                    yield fc


def _collect_frames_for_bone(action, bone_name: str):
    frames = set()
    if not action or not bone_name:
        return frames

    # Match this bone's fcurves (e.g., pose.bones["Bone.L"].location, rotation_quaternion, etc.)
    bone_path_prefix = f'pose.bones["{bone_name}"]'
    for fc in _iter_action_fcurves(action):
        if not fc.data_path.startswith(bone_path_prefix):
            continue
        for kp in getattr(fc, "keyframe_points", []):
            frames.add(int(round(kp.co[0])))
    return frames


def _pose_bone_selected(pose_bone):
    """Return whether the pose bone is selected in Blender 5.0."""
    return pose_bone.select


def _set_pose_bone_selected(pose_bone, value: bool):
    """Set pose bone selection in Blender 5.0."""
    pose_bone.select = value


def _duplicate_end_to_start(scene, obj, bone_names: set[str], cycle_frames: int):
    """Copy target side pose from frame (cycle_frames+1) to frame 1 to close the loop."""
    if cycle_frames < 1 or not bone_names:
        return
    end_frame = cycle_frames + 1
    _set_selection(obj, bone_names)
    scene.frame_set(end_frame)
    bpy.ops.pose.copy()
    scene.frame_set(1)
    _set_selection(obj, bone_names)
    bpy.ops.pose.paste(flipped=False)
    bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')


def _set_selection(obj, names: set[str]):
    """Select only the given pose bones."""
    for pb in obj.pose.bones:
        _set_pose_bone_selected(pb, pb.name in names)
    # set active bone to one of selected for ops that need it
    if names:
        first = next(iter(names))
        obj.data.bones.active = obj.data.bones.get(first)


class ANIFLIP_OT_cycle_mirror(bpy.types.Operator):
    """Mirror keys from one side to the other with a half-cycle offset."""
    bl_idname = "aniflip.cycle_mirror"
    bl_label = "Cycle Mirror"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj
            and obj.type == "ARMATURE"
            and obj.mode == "POSE"
            and obj.animation_data
            and obj.animation_data.action is not None
        )

    def execute(self, context):
        scene = context.scene
        obj = context.active_object
        action = obj.animation_data.action

        cycle_frames = int(getattr(scene, "aniflip_cycle_frames", 0) or 0)
        if cycle_frames < 2:
            self.report({'ERROR'}, "Cycle frames must be at least 2")
            return {'CANCELLED'}
        half = floor(cycle_frames / 2)
        if half < 1:
            self.report({'ERROR'}, "Cycle frames too small for mirror offset")
            return {'CANCELLED'}

        direction = getattr(scene, "aniflip_direction", "RL")
        src_suffix = ".R" if direction == "RL" else ".L"
        dst_suffix = ".L" if src_suffix == ".R" else ".R"

        src_bones = [pb for pb in obj.pose.bones if pb.name.endswith(src_suffix)]
        if not src_bones:
            self.report({'ERROR'}, f"No source bones ending with {src_suffix}")
            return {'CANCELLED'}

        src_to_dst = {}
        for pb in src_bones:
            mirrored = _mirror_name(pb.name)
            if mirrored and mirrored in obj.pose.bones:
                src_to_dst[pb.name] = mirrored
        if not src_to_dst:
            self.report({'ERROR'}, "No mirrored counterparts found for source bones")
            return {'CANCELLED'}

        view_layer = context.view_layer
        view_layer.objects.active = obj
        bpy.ops.object.mode_set(mode="POSE")

        original_frame = scene.frame_current
        original_active = obj.data.bones.active
        original_selection = {pb.name for pb in obj.pose.bones if _pose_bone_selected(pb)}

        try:
            processed_frames = 0
            for src_name, dst_name in src_to_dst.items():
                frames_raw = sorted(_collect_frames_for_bone(action, src_name))
                if not frames_raw:
                    continue
                processed_frames += len(frames_raw)
                for original_frame in frames_raw:
                    targets = set()
                    t = original_frame + half
                    if t > cycle_frames + 1:
                        t -= cycle_frames
                    targets.add(t)

                    # copy pose from source bone at source frame
                    scene.frame_set(original_frame)
                    _set_selection(obj, {src_name})
                    bpy.ops.pose.copy()

                    # paste flipped onto target bone at target frame(s) and insert keys
                    for t in sorted(targets):
                        scene.frame_set(t)
                        _set_selection(obj, {dst_name})
                        bpy.ops.pose.paste(flipped=True)
                        bpy.ops.anim.keyframe_insert_menu(type='LocRotScale')

            # Ensure target side closes the loop: copy end (cycle+1) to frame 1
            _duplicate_end_to_start(scene, obj, set(src_to_dst.values()), cycle_frames)
        finally:
            scene.frame_set(original_frame)
            _set_selection(obj, original_selection)
            obj.data.bones.active = original_active
        self.report({'INFO'}, "Cycle mirror done")
        return {'FINISHED'}
