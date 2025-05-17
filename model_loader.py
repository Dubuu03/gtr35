from OpenGL.GL import *
import numpy as np
import ctypes
import os

def load_model_parts(parts_info, texture_loader):
    loaded_parts = []

    for name, data in parts_info.items():
        # Load vertex and index data from a single .txt file
        with open(data["file"], "r") as f:
            content = f.read()
            local_vars = {}
            exec(content, {}, local_vars)
            vertices = np.array(local_vars["vertices"], dtype=np.float32).flatten()
            indices = np.array(local_vars["indices"], dtype=np.uint32).flatten()

        # --- OpenGL Buffer Setup ---
        VAO = glGenVertexArrays(1)
        VBO = glGenBuffers(1)
        EBO = glGenBuffers(1)

        glBindVertexArray(VAO)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # vertex positions (x, y, z) at location 0
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        # texture coords (u, v) at location 1
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
        glEnableVertexAttribArray(1)

        glBindVertexArray(0)

        # Load texture if specified
        use_texture = data.get("use_texture", False)
        texture_id = 0
        if use_texture:
            texture_path = os.path.join("texture", name + ".png")
            texture_id = texture_loader(texture_path)

        loaded_parts.append({
            "VAO": VAO,
            "EBO": EBO,
            "count": len(indices),
            "texture": texture_id,
            "color": data.get("base_color", [1.0, 1.0, 1.0]),
            "alpha": data.get("alpha", 1.0),
            "roughness": data.get("roughness", 1.0),
            "metallic": data.get("metallic", 0.0),
            "use_texture": use_texture
        })

    return loaded_parts
