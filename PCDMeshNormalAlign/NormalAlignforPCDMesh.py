import bpy
import bmesh
from math import pi
from mathutils import Euler, Vector
import re

def flip_faces_away_from_z_plus(active_obj):
    # Flip all faces whose normals point away from the world Z+ direction (up)
    if bpy.context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(active_obj.data)
    bm.faces.ensure_lookup_table()
    up = Vector((0, 0, 1))
    for f in bm.faces:
        f.select = False
    for f in bm.faces:
        normal_world = active_obj.matrix_world.to_3x3() @ f.normal
        if normal_world.dot(up) < 0:
            f.select = True
    bmesh.update_edit_mesh(active_obj.data)
    bpy.ops.mesh.flip_normals()
    bpy.ops.mesh.select_all(action='DESELECT')

def create_camera_at_empty(cam_name, empty, rot):
    # Delete any existing camera with the same name
    old_cam = bpy.data.objects.get(cam_name)
    if old_cam:
        bpy.data.objects.remove(old_cam, do_unlink=True)
    cam_data = bpy.data.cameras.new(cam_name)
    cam = bpy.data.objects.new(cam_name, cam_data)
    bpy.context.collection.objects.link(cam)
    # Set camera location and rotation before parenting
    cam.location = empty.matrix_world.translation
    cam.rotation_euler = rot
    # Parent the camera to the Empty
    cam.parent = empty
    # After parenting, force the camera's world location and rotation to exactly match the Empty
    cam.matrix_world = empty.matrix_world @ rot.to_matrix().to_4x4()
    return cam

def is_face_visible_from_camera(face, face_center_world, camera_location, active_obj):
    scene = bpy.context.scene
    depsgraph = bpy.context.evaluated_depsgraph_get()
    ray_direction = (face_center_world - camera_location).normalized()
    hit, location, normal, face_index, hit_obj, _ = scene.ray_cast(
        depsgraph, camera_location, ray_direction
    )
    if hit and hit_obj == active_obj and face_index == face.index:
        hit_distance = (location - camera_location).length
        face_distance = (face_center_world - camera_location).length
        if abs(hit_distance - face_distance) < 1.5:
            return True
    return False

def select_backfacing_visible_faces_from_cameras(cameras, active_obj):
    # Select faces that are visible from each camera and whose normals face away from the camera
    if bpy.context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(active_obj.data)
    bm.faces.ensure_lookup_table()
    bm.normal_update()
    obj_matrix = active_obj.matrix_world
    for face in bm.faces:
        face.select = False
    camera_face_indices = set()
    for camera in cameras:
        camera_location = camera.matrix_world.translation
        for face in bm.faces:
            face_center_world = obj_matrix @ face.calc_center_median()
            face_normal_world = obj_matrix.to_3x3() @ face.normal
            to_face = (face_center_world - camera_location).normalized()
            dot_product = face_normal_world.dot(-to_face)
            if dot_product < 0:
                if is_face_visible_from_camera(face, face_center_world, camera_location, active_obj):
                    camera_face_indices.add(face.index)
    for face in bm.faces:
        if face.index in camera_face_indices:
            face.select = True
    bmesh.update_edit_mesh(active_obj.data)

def flip_selected_faces(active_obj):
    # Flip the normals of all selected faces
    if bpy.context.mode != 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(active_obj.data)
    bm.faces.ensure_lookup_table()
    for face in bm.faces:
        if face.select:
            face.normal_flip()
    bmesh.update_edit_mesh(active_obj.data)

def main():
    active_obj = bpy.context.active_object
    if not active_obj or active_obj.type != 'MESH':
        print("Please select a mesh object.")
        return

    # 1. Global flip for faces pointing away from the Z+ direction
    flip_faces_away_from_z_plus(active_obj)

    empty_pattern = re.compile(r'^Empty(\.\d+)?$')
    empties = [obj for obj in bpy.data.objects if obj.type == 'EMPTY' and empty_pattern.match(obj.name)]
    if not empties:
        print("No Empty objects with the name 'Empty' found.")
        return
    rotations = {
        'Cam_X+': Euler((pi/2, 0, pi/2), 'XYZ'),   # +X
        'Cam_X-': Euler((pi/2, 0, -pi/2), 'XYZ'),  # -X
        'Cam_Y+': Euler((pi/2, 0, 0), 'XYZ'),      # +Y
        'Cam_Y-': Euler((pi/2, 0, pi), 'XYZ'),     # -Y
    }
    for empty in empties:
        cameras = []
        for name, rot in rotations.items():
            cam_name = f"{name}_{empty.name}"
            cam = create_camera_at_empty(cam_name, empty, rot)
            cameras.append(cam)
        print(f"Flipping faces based on {empty.name}.")
        select_backfacing_visible_faces_from_cameras(cameras, active_obj)
        flip_selected_faces(active_obj)
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Flip operation completed for all Empty objects and returned to Object mode.")

main()