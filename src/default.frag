#version 330

in vec4 fragColor;
in vec2 fragUV;

out vec4 outColor;

uniform sampler2D tex1;
uniform sampler2D tex2;
uniform float blendRatio;

void main()
{
   vec4 texVal1 = texture(tex1, fragUV);
   vec4 texVal2 = texture(tex2, fragUV);
   outColor = (texVal1 * fragColor * blendRatio / 100) + (texVal2 * fragColor * (100-blendRatio) / 100);
}