import pygltflib
import numpy as np

def extract_material_pbr_data(glb_file_path):
    """Extracts PBR properties from a GLB/GLTF file."""
    # Load the GLB/GLTF file
    glb = pygltflib.GLTF2().load(glb_file_path)

    materials_data = []

    # Iterate through materials in the GLB/GLTF file
    for material in glb.materials:
        material_info = {'name': material.name}
        
        # Extract PBR (Physically-Based Rendering) data
        if material.pbrMetallicRoughness:
            # Base Color (Diffuse color)
            base_color = material.pbrMetallicRoughness.baseColorFactor
            if base_color:
                material_info['Base Color'] = base_color[:3]  # Extract RGB components

            # Metallic
            metallic = material.pbrMetallicRoughness.metallicFactor
            if metallic is not None:
                material_info['Metallic'] = metallic

            # Roughness
            roughness = material.pbrMetallicRoughness.roughnessFactor
            if roughness is not None:
                material_info['Roughness'] = roughness

            # Emissive Color
            emissive_color = material.emissiveFactor
            if emissive_color:
                material_info['Emissive Color'] = emissive_color[:3]  # Extract RGB components

            # Optionally, extract the textures associated with PBR if they exist
            if material.pbrMetallicRoughness.baseColorTexture:
                material_info['Base Color Texture'] = material.pbrMetallicRoughness.baseColorTexture.index
            
            if material.pbrMetallicRoughness.metallicRoughnessTexture:
                material_info['Metallic Roughness Texture'] = material.pbrMetallicRoughness.metallicRoughnessTexture.index

        materials_data.append(material_info)

    return materials_data

def save_material_data_to_file(material_data, output_file):
    """Save material data to a text file."""
    with open(output_file, 'w') as f:
        for material in material_data:
            f.write(f"Material: {material['name']}\n")
            if 'Base Color' in material:
                f.write(f"Base Color (RGB): {material['Base Color']}\n")
            if 'Metallic' in material:
                f.write(f"Metallic: {material['Metallic']}\n")
            if 'Roughness' in material:
                f.write(f"Roughness: {material['Roughness']}\n")
            if 'Emissive Color' in material:
                f.write(f"Emissive Color (RGB): {material['Emissive Color']}\n")
            if 'Base Color Texture' in material:
                f.write(f"Base Color Texture: {material['Base Color Texture']}\n")
            if 'Metallic Roughness Texture' in material:
                f.write(f"Metallic Roughness Texture: {material['Metallic Roughness Texture']}\n")
            f.write("\n")

# Specify the path to your GLTF/GLB file
glb_file_path = 'gtr35v2.glb'  # Change this to your GLB/GLTF file path

# Extract PBR material data from GLTF/GLB file
material_data = extract_material_pbr_data(glb_file_path)

# Specify the output text file
output_file = 'material_pbr_data.txt'  # You can specify any output file path

# Save the extracted data to a text file
save_material_data_to_file(material_data, output_file)

print(f"PBR material data has been saved to {output_file}")
