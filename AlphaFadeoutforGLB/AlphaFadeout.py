import bpy

# Define the number of duplicates
Num = 10# Change this value to adjust the number of duplicates# Enable Backface Culling and set Alpha Blend for the selected objectdef set_backface_culling_and_alpha_blend(obj):
    if obj.active_material:
        mat = obj.active_material
# Enable Backface Culling
        mat.use_backface_culling = True
# Set Alpha Blend
        mat.blend_method = 'BLEND'
        return mat
    else:
        print(f"Object {obj.name} has no active material.")
        return None

# Duplicate the selected object and unlink materialsdef duplicate_object(obj, num):
    new_objects = []
    for i in range(num):
# Duplicate the object
        bpy.ops.object.duplicate(linked=False)
        new_obj = bpy.context.object
        new_objects.append(new_obj)

# Unlink the material (create a unique material for each object)if new_obj.active_material:
            new_material = new_obj.active_material.copy()
            new_obj.active_material = new_material

    return new_objects

# Set the Alpha value of the object's materialdef set_alpha_value(obj, alpha_value):
    if obj.active_material and obj.active_material.node_tree:
        nodes = obj.active_material.node_tree.nodes
        if 'Principled BSDF' in nodes:
# Access Principled BSDF node
            bsdf_node = nodes.get('Principled BSDF')
            bsdf_node.inputs['Alpha'].default_value = alpha_value

# Main function to run the scriptdef main():
# Get the selected object
    selected_obj = bpy.context.active_object
    if not selected_obj:
        print("No object selected.")
        return

# Set Backface Culling and Alpha Blend for the original object
    original_material = set_backface_culling_and_alpha_blend(selected_obj)
    if not original_material:
        print("Selected object has no material, stopping script.")
        return

# Duplicate the object for the number of times specified by 'Num'
    duplicated_objects = duplicate_object(selected_obj, Num)

# Set the Alpha value for each duplicated object and keep them at the same position (0, 0, 0)for i, obj in enumerate([selected_obj] + duplicated_objects):
        alpha_value = 1 - (1/Num) * i
        set_alpha_value(obj, alpha_value)

# Set position to (0, 0, 0)
        obj.location = (0, 0, 0)

        print(f"Object: {obj.name}, Alpha: {alpha_value}")

if __name__ == "__main__":
    main()