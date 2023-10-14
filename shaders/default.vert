#version 330 core

layout (location = 0) in vec3 in_position; //Coordinates of the vertext as a 3d vector. This is related to the vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")]) in model.py

void main() {
    gl_Position = vec4(in_position, 1.0);
}