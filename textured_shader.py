from OpenGL.GL import *

# --- Vertex Shader ---
vertex_shader_src = """
#version 330 core
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec2 aTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec2 TexCoord;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
    TexCoord = aTexCoord;
}
"""

# --- Fragment Shader ---
fragment_shader_src = """
#version 330 core
in vec2 TexCoord;
out vec4 FragColor;

uniform sampler2D texture1;
uniform vec3 baseColor;
uniform float alpha;
uniform float roughness;
uniform float metallic;
uniform bool useTexture;

void main()
{
    vec4 texColor = texture(texture1, TexCoord);
    vec3 finalColor = useTexture ? texColor.rgb : baseColor;
    FragColor = vec4(finalColor, alpha);
}
"""

# --- Shader Compilation Helpers ---
def compile_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if glGetShaderiv(shader, GL_COMPILE_STATUS) != GL_TRUE:
        raise RuntimeError(glGetShaderInfoLog(shader).decode())
    return shader

def create_shader_program():
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_shader_src)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_shader_src)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
        raise RuntimeError(glGetProgramInfoLog(program).decode())

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program
