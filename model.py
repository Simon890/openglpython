import numpy as np
from main import GraphicsEngine

class Triangle:
    def __init__(self, app : GraphicsEngine) -> None:
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
    
    def render(self):
        self.vao.render()
        
    def destroy(self):
        #We need to release the resources since OpenGL doesn't have a garbage collector
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()
    
    def get_vao(self):
        #3f = Buffer format, in_position = Attributes
        #3f each vertext is assign 3 floating numbers and these correspont to in_position attribute
        #vao = Vertext Array Object => We associate the vertext object (VBO) with Shader program
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")])
        return vao
    
    def get_vertex_data(self):
        #coordinates     x     y    z
        #opengl uses right handed coordinate system
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype="f4")
        return vertex_data
    
    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        #Send data to the GPU memory
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertext_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()
        
        program = self.ctx.program(vertex_shader=vertext_shader, fragment_shader=fragment_shader)#Compile our shader using CPU
        return program