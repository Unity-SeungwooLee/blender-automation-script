import bpy
from mathutils import Vector

column = 16
row = 4

#Switch column and row offsets
offset = Vector((1/column, 0))
#offset = Vector((0, 1/row))


# Get object and UV map given the selected object
def GetSelectedObjectAndUVMap(uvMapName):
    try:
        # Get the active object from selection
        obj = bpy.context.active_object

        if obj and obj.type == 'MESH':
            uvMap = obj.data.uv_layers[uvMapName]
            return obj, uvMap
    except:
        pass

    return None, None


# Add offset to the UV map
def OffsetUV(uvMap, offset):
    for uvIndex in range(len(uvMap.data)):
        # Add the offset to the UV
        uvMap.data[uvIndex].uv += offset
        print(f"UV {uvIndex} after offset: {uvMap.data[uvIndex].uv}")

# Main function to create planes and adjust UVs
def main():
    # UV data are not accessible in edit mode
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # The name of the UV map
    uvMapName = 'UVMap'  # Replace with your UV map name
    
    # Get the active selected object and its UV map
    obj, uvMap = GetSelectedObjectAndUVMap(uvMapName)

    if obj is None or uvMap is None:
        print("No valid mesh object or UV map found.")
        return

    # Create a new duplicate of the selected object
    #bpy.ops.object.select_all(action='DESELECT')
    #obj.select_set(True)
    bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked": False, "mode": 'TRANSLATION'})
    new_obj = bpy.context.active_object

    # Add the offset to the new duplicated object’s UV map
    OffsetUV(new_obj.data.uv_layers.active, offset)
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')

if __name__ == "__main__":
    main()
