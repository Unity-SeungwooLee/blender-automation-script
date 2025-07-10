import bpy

# Number of particle systems you want to create
num_particle_systems = 21

# Define the base name of the objects to be used as particle instances
object_name_base = "Suzanne"# Replace "abc" with your desired base name for particle objects# Object names to be used as the instance for each particle system# e.g., "abc", "abc.001", "abc.002", ...
instance_objects = [f"{object_name_base}{'' if i == 0 else f'.{str(i).zfill(3)}'}" for i in range(num_particle_systems)]
print(f"Instance objects list: {instance_objects}")

# Get the selected object
selected_obj = bpy.context.active_object

# Check if an object is selectedif selected_obj is None:
    raise Exception("No object selected. Please select an object in the scene.")

# Main function to add particle systems to the selected objectdef create_particle_systems(obj, num_systems):
    for i in range(num_systems):
# Create a new particle system
        particle_sys = obj.modifiers.new(name=f"ParticleSystem_{i+1}", type='PARTICLE_SYSTEM')
        psys = obj.particle_systems[-1]

# Set the particle system's settings
        psettings = psys.settings
        psettings.count = 1# Number of particles
        psettings.frame_start = i + 1# Frame start increases
        psettings.frame_end = i + 1# Frame end equals frame start
        psettings.lifetime = 1# Particle lifetime set to 1
        psettings.emit_from = 'FACE'# Emit from faces
        psettings.use_emit_random = False# Emit from exactly one face
        psettings.userjit = 1
        psettings.normal_factor = 0# Set velocity normal to 0
        psettings.render_type = 'OBJECT'# Render as object

# Set the instance object for each particle system using the name list
        instance_obj = bpy.data.objects.get(instance_objects[i])
        if instance_obj:
            psettings.instance_object = instance_obj
        else:
            print(f"Warning: {instance_objects[i]} not found. Skipping particle system {i + 1}.")

        psettings.particle_size = 1.0# Set render scale to 1.0
        psettings.use_rotation_instance = True# Use object rotation
        psettings.effector_weights.gravity = 0# Disable gravity# Run the function to create particle systems on the selected object
create_particle_systems(selected_obj, num_particle_systems)

print(f"Created {num_particle_systems} particle systems on {selected_obj.name}")