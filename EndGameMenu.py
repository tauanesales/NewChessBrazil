import pyglet
import pyglet.window.key


class EndGameMenu():
    def __init__(self, width, height, is_checkmate=False, is_draw=False):
        self.width = width
        self.height = height
        self.checkmate = is_checkmate
        self.draw = is_draw
        self.start_btn = pyglet.image.load('public/start.png')
        self.sprite_btn = pyglet.sprite.Sprite(self.start_btn, x=200, y=80)
        self.batch = pyglet.graphics.Batch()

    def on_draw(self):
        if self.checkmate:
            self.background = pyglet.image.load('public/checkmate.jpg')
            self.sprite_bg = pyglet.sprite.Sprite(self.background, x=0, y=0)
            self.text = 'Xeque-mate!'
            self.label = pyglet.text.Label(
                self.text,
                font_name='Comic Sans MS',
                font_size=40,
                x=self.width/2, y=self.height - 80,
                anchor_x='center', anchor_y='center'
            )

        elif self.draw:
            self.background = pyglet.image.load('public/draw.png')
            self.sprite_bg = pyglet.sprite.Sprite(
                self.background,
                x=0,
                y=0
            )
            self.text = 'Empate!'
            self.label = pyglet.text.Label(
                self.text,
                font_name='Comic Sans MS',
                font_size=40,
                x=self.width/2, y=self.height - 80,
                anchor_x='center', anchor_y='center'
            )
            self.label.color = (245, 189, 31, 255)

        self.sprite_bg.draw()
        self.label.draw()
        self.sprite_btn.draw()

    def on_mouse_release(self, x, y):
        if 200 <= x <= 312 and 80 <= y <= 131:
            return 'game'
        else:
            return 'end-game'
