#version 330

in vec4 fragColor;
in vec2 fragUV;
in vec3 fragNormal;
in vec3 fragPos;

out vec4 outColor;

uniform sampler2D tex1;
uniform vec3 eyePos;
uniform bool isBlinn;

uniform vec3 dLightDir;
uniform vec4 dLightColor;
uniform float dLightIntensity;
uniform float dLightIsOn;

uniform vec3 pLightPos;
uniform vec4 pLightColor;
uniform float pLightIntensity;
uniform float pLightIsOn;

uniform vec3 sLightPos;
uniform vec4 sLightColor;
uniform vec3 sDir;
uniform float sLightIntensity;
uniform float sLightCutoff;
uniform float sLightIsOn;



void main()
{
    vec3 eyeDir = normalize(eyePos - fragPos);

    vec4 texVal = texture(tex1, fragUV);
    // simple lambert diffuse shading model
    float nDotDL = max(dot((fragNormal), normalize(dLightDir)), 0.0);

    float shininess = 1.0;
    vec3 dHalfwayDir = normalize(dLightDir + eyeDir);
    float dSpec = pow(max(dot(fragNormal, dHalfwayDir), 0.0), shininess);
    float dLightEffect;

    if(isBlinn)
    {
        dLightEffect = nDotDL + dSpec;
    } 
    else
    {
        dLightEffect = nDotDL;
    }
    
    vec4 dTerm = fragColor * texVal * dLightColor * dLightIntensity * dLightEffect * dLightIsOn;

    
    vec3 pLightDir = normalize(pLightPos - fragPos);
    float nDotPL = max(dot((fragNormal), normalize(pLightDir)), 0.0);

    shininess = 1.0;
    vec3 pHalfwayDir = normalize(pLightDir + eyeDir);
    float pSpec = pow(max(dot(fragNormal, pHalfwayDir), 0.0), shininess);
    float pLightEffect;

    if(isBlinn)
    {
        pLightEffect = nDotPL + pSpec;
    } 
    else
    {
        pLightEffect = nDotPL;
    }

    vec4 pTerm = fragColor * texVal * pLightColor * pLightIntensity * pLightEffect * pLightIsOn;


    vec3 sLightDir = normalize(fragPos - sLightPos);
    float sCosTheta = dot(normalize(sDir), normalize(sLightDir));
    vec4 sTerm;

    if(sCosTheta > sLightCutoff) 
    {       
        
        float nDotSL = max(dot((fragNormal), normalize(-sLightDir)), 0.0);
        shininess = 1.0;
        vec3 sHalfwayDir = normalize(sLightDir + eyeDir);
        float sSpec = pow(max(dot(fragNormal, sHalfwayDir), 0.0), shininess);
        float sLightEffect;

        if(isBlinn)
        {
            sLightEffect = nDotSL + sSpec;
        } 
        else
        {
            sLightEffect = nDotSL;
        }
        sTerm = fragColor * texVal * sLightColor * sLightIntensity * sLightEffect * sCosTheta * sLightIsOn;
        
    }
    else
    {
        sTerm = vec4(0.0, 0.0, 0.0, 0.0);
    }

    outColor = dTerm + pTerm + sTerm;
}