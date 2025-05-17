def extract_obj_to_txt(obj_path, vertex_output, index_output):
    vertices = []
    texcoords = []
    faces = []

    with open(obj_path, 'r') as file:
        for line in file:
            if line.startswith("v "):
                parts = line.strip().split()
                vertices.append(list(map(float, parts[1:4])))
            elif line.startswith("vt "):
                parts = line.strip().split()
                texcoords.append(list(map(float, parts[1:3])))
            elif line.startswith("f "):
                parts = line.strip().split()[1:]
                face = []
                for part in parts:
                    vals = part.split('/')
                    if len(vals) >= 2:
                        v = int(vals[0]) - 1
                        t = int(vals[1]) - 1
                        face.append((v, t))
                # Triangulate if more than 3 vertices
                for i in range(1, len(face) - 1):
                    faces.append([face[0], face[i], face[i + 1]])

    final_vertices = []
    index_map = {}
    indices = []
    index = 0

    for face in faces:
        for v_idx, t_idx in face:
            key = (v_idx, t_idx)
            if key not in index_map:
                index_map[key] = index
                final_vertices.extend(vertices[v_idx] + texcoords[t_idx])
                index += 1
            indices.append(index_map[key])

    with open(vertex_output, 'w') as f:
        for i in range(0, len(final_vertices), 5):
            f.write(f"{final_vertices[i]:.6f},{final_vertices[i+1]:.6f},{final_vertices[i+2]:.6f},"
                    f"{final_vertices[i+3]:.6f},{final_vertices[i+4]:.6f}\n")

    with open(index_output, 'w') as f:
        for i in range(0, len(indices), 3):
            if i + 2 < len(indices):
                f.write(f"{indices[i]},{indices[i+1]},{indices[i+2]}\n")

if __name__ == "__main__":
    extract_obj_to_txt("gtr35.obj", "gtr35_vertices_uv.txt", "gtr35_indices_uv.txt")
