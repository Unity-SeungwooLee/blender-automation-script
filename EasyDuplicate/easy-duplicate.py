import bpy
import mathutils
import random
from math import radians
from bpy_extras.view3d_utils import region_2d_to_vector_3d, region_2d_to_origin_3d

# Configuration variables
ObjectA = "TreeA"
ObjectB = "TreeB"
Zrotate = True  # Set to True for random Z rotation, False for no rotation

def get_mouse_ray(context, event):
    """Calculate ray origin and direction from the mouse point in 3D view"""
    region = context.region
    region_3d = context.space_data.region_3d
    
    # Get the 2D mouse coordinates
    coord = (event.mouse_region_x, event.mouse_region_y)
    
    # Calculate the ray origin and direction using bpy_extras utilities
    ray_origin = region_2d_to_origin_3d(region, region_3d, coord)
    ray_direction = region_2d_to_vector_3d(region, region_3d, coord)
    
    return ray_origin, ray_direction

def place_tree(context, event, object_name):
    """Ray cast from the mouse point and place a tree at the hit location"""
    # Get the object to duplicate
    object_template = bpy.data.objects.get(object_name)
    
    if object_template:
        # Get the ray origin and direction from the mouse click
        ray_origin, ray_direction = get_mouse_ray(context, event)
        
        # Cast the ray from the mouse point
        depsgraph = context.evaluated_depsgraph_get()
        result, location, normal, index, object, matrix = context.scene.ray_cast(
            depsgraph, ray_origin, ray_direction)
        
        if result:
            # Duplicate the object and place it at the hit location
            new_object = object_template.copy()
            new_object.data = object_template.data.copy()
            new_object.location = location
            
            # Apply random Z rotation if enabled
            if Zrotate:
                random_angle = random.uniform(0, 360)  # Random angle between 0 and 360 degrees
                new_object.rotation_euler[2] = radians(random_angle)  # Apply rotation in radians
            
            context.collection.objects.link(new_object)
            print(f"{object_name} placed at {location}" + (f" with {random_angle:.1f}° rotation" if Zrotate else ""))
        else:
            print("No valid surface detected to place the object.")
    else:
        print(f"Error: Object not found. Make sure the object is named '{object_name}'")

class PlaceTreeOperator(bpy.types.Operator):
    """Place Objects on Mouse Click - Left Click for ObjectA, Shift+Left Click for ObjectB"""
    bl_idname = "object.place_tree"
    bl_label = "Place Object Operator"
    
    def modal(self, context, event):
        # Exit when pressing the right mouse button or ESC
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        
        # Place object when left mouse button is clicked
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            if event.shift:
                place_tree(context, event, ObjectB)  # Place ObjectB with Shift+Left Click
            else:
                place_tree(context, event, ObjectA)  # Place ObjectA with Left Click
            return {'RUNNING_MODAL'}
        
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            context.window_manager.modal_handler_add(self)
            print("Object Placement Active - Left Click for ObjectA, Shift+Left Click for ObjectB, Right Click/ESC to exit")
            return {'RUNNING_MODAL'}
        else:
            self.report({'ERROR'}, "Operator only works in the 3D Viewport.")
            return {'CANCELLED'}

# Add keyboard shortcut
addon_keymaps = []

def register():
    bpy.utils.register_class(PlaceTreeOperator)
    
    # Add the keymap
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(
            PlaceTreeOperator.bl_idname,
            type='F',
            value='PRESS',
            shift=True
        )
        addon_keymaps.append((km, kmi))

def unregister():
    # Remove the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    bpy.utils.unregister_class(PlaceTreeOperator)

if __name__ == "__main__":
    register()