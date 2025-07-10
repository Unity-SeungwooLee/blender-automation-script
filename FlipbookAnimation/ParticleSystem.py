import bpy

# Number of particle systems you want to create
num_particle_systems = 64

# Object names to be used as the instance for each particle system
instance_objects = [f"Plane{'' if i == 0 else f'.{str(i).zfill(3)}'}" for i in range(num_particle_systems)]

# Get the selected object (or replace with the name of the object manually)
obj = bpy.context.active_object

# Main function to add particle systems
def create_particle_systems(obj, num_systems):
    for i in range(num_systems):
        # Create a new particle system
        particle_sys = obj.modifiers.new(name=f"ParticleSystem_{i+1}", type='PARTICLE_SYSTEM')
        psys = obj.particle_systems[-1]
        
        # Set the particle system's settings
        psettings = psys.settings
        psettings.count = 1  # Number of particles
        psettings.frame_start = i + 1  # Frame start increases
        psettings.frame_end = i + 1  # Frame end equals frame start
        psettings.lifetime = 1  # Particle lifetime set to 1
        psettings.emit_from = 'FACE'  # Emit from faces
        psettings.use_emit_random = False  # Emit from exactly one face
        psettings.userjit = 1
        psettings.normal_factor = 0  # Set velocity normal to 0
        psettings.render_type = 'OBJECT'  # Render as object
        psettings.instance_object = bpy.data.objects.get(instance_objects[i])  # Set the instance object
        psettings.particle_size = 1.0  # Set render scale to 1.0
        psettings.use_rotation_instance = True  # Use object rotation
        psettings.effector_weights.gravity = 0  # Disable gravity

# Run the function
create_particle_systems(obj, num_particle_systems)

print(f"Created {num_particle_systems} particle systems on {obj.name}")