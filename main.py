import pygame as pg
import moderngl as mgl
import sys
from model import *

class GraphicsEngine:
    def __init__(self, win_size=(1600, 900)):
        #init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        #set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3) #Version 3
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3) #Version 3
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE) #Not use deprecated functionality
        #create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        #Detect and use existing opengl
        self.ctx = mgl.create_context()
        #create an object to help track time
        self.clock = pg.time.Clock()
        #scene
        self.scene = Triangle(self)
        
    def check_events(self):
        for event in pg.event.get():
            #Close the window or press the escape key
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()
    
    def render(self):
        #clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18)) #Fill the screen with the selected color
        #render scene
        self.scene.render()
        #swap buffers   
        pg.display.flip()
    
    def run(self):
        while True:
            self.check_events()
            self.render()
            self.clock.tick(60) #Set framerate
        
if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()    