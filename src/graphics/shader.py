"""
Shader management for Modern OpenGL
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import OpenGL.GL as gl


class Shader:
    """Represents a compiled GLSL shader program"""
    
    def __init__(self, vertex_path, fragment_path):
        self.program = None
        self.compile_shader(vertex_path, fragment_path)
    
    def compile_shader(self, vertex_path, fragment_path):
        """Compile and link shader program"""
        try:
            # Read shader files
            with open(vertex_path, 'r') as f:
                vertex_source = f.read()
            with open(fragment_path, 'r') as f:
                fragment_source = f.read()
            
            # Compile vertex shader
            vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
            gl.glShaderSource(vertex, vertex_source)
            gl.glCompileShader(vertex)
            if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
                error = gl.glGetShaderInfoLog(vertex).decode()
                raise ValueError(f"Vertex shader compilation failed:\n{error}")
            
            # Compile fragment shader
            fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
            gl.glShaderSource(fragment, fragment_source)
            gl.glCompileShader(fragment)
            if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
                error = gl.glGetShaderInfoLog(fragment).decode()
                raise ValueError(f"Fragment shader compilation failed:\n{error}")
            
            # Link program
            self.program = gl.glCreateProgram()
            gl.glAttachShader(self.program, vertex)
            gl.glAttachShader(self.program, fragment)
            gl.glLinkProgram(self.program)
            if not gl.glGetProgramiv(self.program, gl.GL_LINK_STATUS):
                error = gl.glGetProgramInfoLog(self.program).decode()
                raise ValueError(f"Shader program linking failed:\n{error}")
            
            gl.glDeleteShader(vertex)
            gl.glDeleteShader(fragment)
            print(f"✓ Shader compiled successfully: {vertex_path}")
        except Exception as e:
            print(f"✗ Shader compilation error: {e}")
            print(f"  Vertex: {vertex_path}")
            print(f"  Fragment: {fragment_path}")
            raise
    
    def use(self):
        """Use this shader program"""
        gl.glUseProgram(self.program)
    
    def set_mat4(self, name, mat4):
        """Set a 4x4 matrix uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniformMatrix4fv(loc, 1, gl.GL_TRUE, mat4)
    
    def set_vec3(self, name, x, y, z):
        """Set a 3D vector uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform3f(loc, x, y, z)
    
    def set_vec4(self, name, x, y, z, w):
        """Set a 4D vector uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform4f(loc, x, y, z, w)
    
    def set_vec2(self, name, x, y):
        """Set a 2D vector uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform2f(loc, x, y)
    
    def set_float(self, name, value):
        """Set a float uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform1f(loc, value)
    
    def set_int(self, name, value):
        """Set an integer uniform"""
        loc = gl.glGetUniformLocation(self.program, name)
        gl.glUniform1i(loc, value)
    
    def delete(self):
        """Delete the shader program"""
        gl.glDeleteProgram(self.program)


class ShaderManager:
    """Manages all shaders in the game"""
    
    def __init__(self):
        self.shaders = {}
        self.load_shaders()
    
    def load_shaders(self):
        """Load all shaders"""
        base_path = os.path.dirname(os.path.abspath(__file__))
        shaders_path = os.path.join(base_path, 'shaders')
        
        # Load standard shader (for textured objects)
        self.shaders['standard'] = Shader(
            os.path.join(shaders_path, 'standard.vert'),
            os.path.join(shaders_path, 'standard.frag')
        )
        
        # Load simple shader (for colored objects)
        self.shaders['simple'] = Shader(
            os.path.join(shaders_path, 'simple.vert'),
            os.path.join(shaders_path, 'simple.frag')
        )
    
    def get_shader(self, name):
        """Get a shader by name"""
        return self.shaders.get(name)
    
    def cleanup(self):
        """Delete all shader programs"""
        for shader in self.shaders.values():
            shader.delete()
