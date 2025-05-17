import pygame
from pygame.locals import *
from OpenGL.GL import *
import glm
import config
from textured_shader import create_shader_program
from texture_loader import load_texture
from model_loader import load_model_parts
import json

def main():
    # Initialize Pygame and OpenGL
    pygame.init()
    display = (config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)
    glClearColor(*config.BACKGROUND_COLOR)

    # Compile and use shader program
    shader = create_shader_program()
    glUseProgram(shader)

    # Load model parts from info.json
    with open("info.json", "r") as f:
        parts_info = json.load(f)

    parts = load_model_parts(
        parts_info,
        lambda name: load_texture(f"texture/{name}.png")  # Load texture from folder
    )

    # Uniform locations
    model_loc = glGetUniformLocation(shader, "model")
    view_loc = glGetUniformLocation(shader, "view")
    proj_loc = glGetUniformLocation(shader, "projection")
    color_loc = glGetUniformLocation(shader, "baseColor")
    use_tex_loc = glGetUniformLocation(shader, "useTexture")

    # Camera setup
    view = glm.lookAt(glm.vec3(3, 2, 6), glm.vec3(0, 0.5, 0), glm.vec3(0, 1, 0))
    proj = glm.perspective(glm.radians(60.0), display[0]/display[1], 0.1, 100.0)

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(proj))

    # Render loop
    angle = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Rotation
        model = glm.rotate(glm.mat4(1.0), glm.radians(angle), glm.vec3(0.0, 1.0, 0.0))
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))

        # Draw all parts
        for part in parts:
            glUniform3fv(color_loc, 1, part["color"])
            glUniform1i(use_tex_loc, part["use_texture"])
            if part["use_texture"]:
                glBindTexture(GL_TEXTURE_2D, part["texture"])
            glBindVertexArray(part["VAO"])
            glDrawElements(GL_TRIANGLES, part["count"], GL_UNSIGNED_INT, None)

        pygame.display.flip()
        clock.tick(config.FPS)
        angle += 1

    # Cleanup
    pygame.quit()

if __name__ == "__main__":
    main()
