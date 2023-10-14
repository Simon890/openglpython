import glm

class BaseModel:
    def __init__(self, app, vao_name, text_id) -> None:
        self.app = app
        self.m_model = self.get_model_matrix()
        self.text_id = text_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera
        
    def update(self): ...
    
    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, vao_name = "cube", text_id = 0) -> None:
        super().__init__(app, vao_name, text_id)
        self.on_init()
    
    def update(self):
        self.texture.use()
        self.program["camPos"].write(self.camera.position)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        
    def on_init(self):
        #Exports variables to shaders
        #texture
        self.texture = self.app.mesh.texture.textures[self.text_id]
        self.program["u_texture_0"] = 0
        self.texture.use(0)
        #mvp
        self.program["m_proj"].write(self.camera.m_proj)
        self.program["m_view"].write(self.camera.m_view)
        self.program["m_model"].write(self.m_model)
        #light
        self.program["light.position"].write(self.app.light.position)
        self.program["light.Ia"].write(self.app.light.Ia)
        self.program["light.Id"].write(self.app.light.Id)
        self.program["light.Is"].write(self.app.light.Is)
      