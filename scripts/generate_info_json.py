import os
import json
from extract_gtr35_multi import parse_pbr_data

# Config
PARTS_DIR = "gtr35_parts"
PBR_PATH = "material_pbr_data.txt"
OUT_PATH = f"{PARTS_DIR}/info.json"

def generate_info_json():
    pbr_data = parse_pbr_data(PBR_PATH)
    parts = {}

    for file in os.listdir(PARTS_DIR):
        if file.endswith("_vertices.txt"):
            name = file.replace("_vertices.txt", "")
            vertices_file = os.path.join(PARTS_DIR, file)
            indices_file = os.path.join(PARTS_DIR, f"{name}_indices.txt")

            if os.path.exists(indices_file):
                parts[name] = {
                    "vertices_file": vertices_file,
                    "indices_file": indices_file,
                    "use_texture": pbr_data.get(name, {}).get("use_texture", False),
                    "base_color": pbr_data.get(name, {}).get("base_color", [1.0, 1.0, 1.0])
                }

    with open(OUT_PATH, "w") as f:
        json.dump(parts, f, indent=2)
    print(f"Saved to: {OUT_PATH}")

if __name__ == "__main__":
    generate_info_json()
