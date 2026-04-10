#version 330 core

in vec3 vFragPos;

uniform vec3 uColor;
uniform vec3 uViewPos;

out vec4 FragColor;

void main()
{
    vec3 color = uColor;
    
    // Fog effect
    float distance = length(vFragPos - uViewPos);
    float fogFactor = exp(-0.001 * distance * distance);
    vec3 fogColor = vec3(0.53, 0.76, 0.98);
    color = mix(fogColor, color, fogFactor);
    
    FragColor = vec4(color, 1.0);
}
