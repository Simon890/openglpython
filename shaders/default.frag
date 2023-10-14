#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;

uniform sampler2D u_texture_0; //Texture that comes from self.shader_program["u_texture_0"] = 0

void main() {
    //vec3 color = vec3(uv_0, 0); For when we don't have a texture
    vec3 color = texture(u_texture_0, uv_0).rgb; //Get the color to the specified fragment
    fragColor = vec4(color, 1.0);
}