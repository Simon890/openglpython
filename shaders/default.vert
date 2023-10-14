#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_normal;
layout (location = 2) in vec3 in_position; //Coordinates of the vertext as a 3d vector. This is related to the vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")]) in model.py

out vec2 uv_0; //Texture coordinates for the fragment shader (default.frag)
out vec3 normal;
out vec3 fragPos;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main() {
    uv_0 = in_texcoord_0;
    fragPos = vec3(m_model * vec4(in_position, 1.0));
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);
}