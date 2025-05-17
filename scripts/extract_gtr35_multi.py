import os
import re
from collections import defaultdict

def parse_pbr_data(pbr_file_path):
    with open(pbr_file_path, "r") as f:
        lines = f.readlines()

    materials = {}
    current = None
    for line in lines:
        if line.startswith("Material:"):
            current = line.split(":", 1)[1].strip()
            materials[current] = {}
        elif "Base Color (RGB)" in line:
            rgb = re.findall(r"[\d.]+", line)
            materials[current]['base_color'] = list(map(float, rgb))
        elif "Base Color Texture" in line:
            materials[current]['use_texture'] = True

    return materials

def extract_multi_material_obj(obj_path, mtl_data_path, out_dir="gtr35_parts"):
    os.makedirs(out_dir, exist_ok=True)
    materials_info = parse_pbr_data(mtl_data_path)

    vertices, texcoords = [], []
    materials = defaultdict(list)
    current_mtl = None

    with open(obj_path, "r") as f:
        for line in f:
            if line.startswith("v "):
                vertices.append(list(map(float, line.strip().split()[1:4])))
            elif line.startswith("vt "):
                texcoords.append(list(map(float, line.strip().split()[1:3])))
            elif line.startswith("usemtl"):
                current_mtl = line.strip().split()[1]
            elif line.startswith("f ") and current_mtl:
                face = [tuple(map(lambda x: int(x) - 1, part.split('/')[:2])) for part in line.strip().split()[1:]]
                for i in range(1, len(face) - 1):
                    materials[current_mtl].append([face[0], face[i], face[i + 1]])

    for mtl, faces in materials.items():
        vmap, final_vertices, indices = {}, [], []
        index = 0
        for face in faces:
            for v_idx, t_idx in face:
                key = (v_idx, t_idx)
                if key not in vmap:
                    vmap[key] = index
                    final_vertices.append(vertices[v_idx] + texcoords[t_idx])
                    index += 1
                indices.append(vmap[key])

        with open(f"{out_dir}/{mtl}.txt", "w") as f:
            # Write vertices
            f.write("vertices = [\n")
            for v in final_vertices:
                f.write(f"    [{v[0]:.6f}, {v[1]:.6f}, {v[2]:.6f}, {v[3]:.6f}, {v[4]:.6f}],\n")
            f.write("]\n\n")

            # Write indices
            f.write("indices = [\n")
            for i in range(0, len(indices), 3):
                f.write(f"    {indices[i]}, {indices[i+1]}, {indices[i+2]},\n")
            f.write("]\n")

        print(f"Saved: {mtl}.txt")

if __name__ == "__main__":
    extract_multi_material_obj("blender_files/gtr35.obj", "blender_files/material_pbr_data.txt")
