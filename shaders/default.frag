#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
in vec3 fragPos;


struct Light {
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

uniform Light light;
uniform sampler2D u_texture_0; //Texture that comes from self.shader_program["u_texture_0"] = 0
uniform vec3 camPos;

vec3 getLight(vec3 color) {
    vec3 Normal = normalize(normal);
    //Ambient light
    vec3 ambient = light.Ia;
    //Diffuse light
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    //specular light
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32); //32 determens the strenght of shining
    vec3 specular = spec * light.Is;

    return color * (ambient + diffuse + specular);
}

void main() {
    //vec3 color = vec3(uv_0, 0); For when we don't have a texture
    vec3 color = texture(u_texture_0, uv_0).rgb; //Get the color to the specified fragment
    color = getLight(color);
    fragColor = vec4(color, 1.0);
}