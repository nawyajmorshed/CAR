#version 330 core

in vec3 vFragPos;
in vec3 vNormal;
in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec3 uViewPos;
uniform vec3 uLightDirection;
uniform vec3 uLightColor;
uniform float uAmbient;

out vec4 FragColor;

void main()
{
    // Sample texture
    vec4 texColor = texture(uTexture, vTexCoord);
    if(texColor.a < 0.1) discard;
    
    // Normalize vectors
    vec3 norm = normalize(vNormal);
    vec3 lightDir = normalize(-uLightDirection);
    
    // Ambient
    vec3 ambient = uAmbient * texColor.rgb;
    
    // Diffuse
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * uLightColor * texColor.rgb;
    
    // Specular
    vec3 viewDir = normalize(uViewPos - vFragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32.0);
    vec3 specular = spec * uLightColor * 0.5;
    
    // Combine
    vec3 result = ambient + diffuse + specular;
    
    // Fog effect
    float distance = length(vFragPos - uViewPos);
    float fogFactor = exp(-0.001 * distance * distance);
    vec3 fogColor = vec3(0.53, 0.76, 0.98);
    result = mix(fogColor, result, fogFactor);
    
    FragColor = vec4(result, 1.0);
}
