import numpy as np
from main import GraphicsEngine
import glm
import pygame as pg

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
    
class Cube:
    def __init__(self, app : GraphicsEngine) -> None:
        self.app = app
        self.ctx = app.ctx
        self.vbo = self.get_vbo()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vao()
        self.m_model = self.get_model_matrix()
        self.texture = self.get_texture(path="textures/img.png")
        self.on_init()
        
    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True) #Flip on Y because pygame has different axis
        #                          Texture size            Colors components   Texture as string
        texture = self.ctx.texture(size=texture.get_size(), components=3, data=pg.image.tostring(texture, "RGB"))
        return texture
        
    def update(self):
        #Generate rotation and update the matrix_model
        m_model = glm.rotate(self.m_model, self.app.time * 0.5, glm.vec3(0, 1, 0))
        self.shader_program["m_model"].write(m_model)
        self.shader_program["m_view"].write(self.app.camera.m_view) #Update m_view since we can move the camera position
        
    def get_model_matrix(self):
        #Generate matrix_model as an identity matrix 4x4
        m_model = glm.mat4() #Identity matrix 4x4
        return m_model
    
    def on_init(self):
        #Exports variables to shaders
        #texture
        self.shader_program["u_texture_0"] = 0 #Number of the texture unit
        self.texture.use(0) #Bind texture location
        #mvp
        self.shader_program["m_proj"].write(self.app.camera.m_proj)
        self.shader_program["m_view"].write(self.app.camera.m_view)
        self.shader_program["m_model"].write(self.m_model)
    
    def render(self):
        self.update()
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
        #vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "3f", "in_position")]) Before adding texture
        vao = self.ctx.vertex_array(self.shader_program, [(self.vbo, "2f 3f", 'in_texcoord_0', 'in_position')])
        return vao
    
    def get_vertex_data(self):
        #coordinates     x     y    z
        #opengl uses right handed coordinate system
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                       (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2), 
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.array(vertex_data, dtype="f4")
        
        #Set texture
        tex_coord = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        text_coord_data = self.get_data(tex_coord, tex_coord_indices)
        vertex_data = np.hstack([text_coord_data, vertex_data]) #Combine the geometry and texture data
        return vertex_data
    
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triange in indices for ind in triange]
        return np.array(data, dtype="f4")
    
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