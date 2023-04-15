from random import choice, randint
from pygame import*
font.init()


class GameSprite (sprite.Sprite):
    def __init__(self, sprite_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        virtual_surface.blit(self.image, (self.rect.x, self.rect.y))

class Platform(GameSprite):
    def __init__(self, x, y, player):
        super(). __init__("images/platform.png", x, y, 150, 20, 15)
        if player == 1:
            self.angle = -90
        if player == 2:
            self.angle = 90
        self.image = transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.player = player

    def update(self):
        keys_pressed = key.get_pressed()

        if self.player == 1:
            if keys_pressed[K_w] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys_pressed[K_s] and self.rect.y < HEIGHT - self.rect.height:
                self.rect.y += self.speed

        if self.player == 2:
            if keys_pressed[K_UP] and self.rect.y > 5:
                self.rect.y -= self.speed
            if keys_pressed[K_DOWN] and self.rect.y < HEIGHT - self.rect.height:
                self.rect.y += self.speed


class Ball(GameSprite):
    def __int__(self):
        super(). __init__("image/ ball.png", 575, 325, 50, 50, 10)
        self.speed = 10
        self.speed_x = self.speed
        self.speed_y = self.speed
        self.disabled = True
        self.wait = 0

    def update(self):
        global score_2
        global score_1

        global text_score_1
        global text_score_2

        if self.wait <= 0:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        else:
            self.wait -= 1

        if self.rect.y >= HEIGHT - self.rect.height or self.rect.y <= 0:
            self.speed_y *= -1

        if ball.rect.colliderect(platform_2.rect) or ball.rect.colliderect(platform_1.rect):
            self.speed_x *= -1.05
            self.speed_y = randint(-10, 10)
        if ball.rect.x >= WIDTH:
            self.respawn()
            score_1 += 1
            text_score_1 = font_score.render(str(score_1), True, (0, 0, 0))
        if ball.rect.x <= -self.rect.width:
            self.respawn()
            score_2 += 1
            text_score_2 = font_score.render(str(score_2), True, (0, 0, 0))

        if self.disabled:
            self.disabled = False
            self.wait = 60

    def respawn(self):
        self.rect.x = 575
        self.rect.y = 325

        self.speed_y = choice((-self.speed, self.speed))
        self.speed_x = choice((-self.speed, self.speed))

        self.disabled = True



WIDTH = 1200
HEIGHT = 700


ASPECT_RATIO = WIDTH / HEIGHT

clock = time.Clock()
fps = 60

back = (106, 245, 168)

window = display.set_mode((WIDTH, HEIGHT), RESIZABLE)
display.set_caption("Ping-Pong")

current_size = window.get_size()
virtual_surface = Surface((WIDTH, HEIGHT))

game = True

ball = Ball()

platform_1 = Platform(100,275, 1)
platform_2 = Platform(1100, 275, 2)

score_1 = 0
score_2 = 0
font_score = font.Font(None, 50)

text_score_1 = font_score.render(str(score_1), True, (0, 0, 0))
text_score_2 = font_score.render(str(score_2), True, (0, 0, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
        if e.type == VIDEORESIZE:
            new_width = e.w
            new_height = int(new_width / ASPECT_RATIO)
            window = display.set_mode((new_width, new_height), RESIZABLE)
            current_size = window.get_size()

    virtual_surface.fill(back)
    ball.update()
    ball.reset()

    platform_1.update()
    platform_1.reset()

    platform_2.update()
    platform_2.reset()
    
    virtual_surface.blit(text_score_1, (550, 20))
    virtual_surface.blit(text_score_2, (640, 20))

    scaled_surface = transform.scale(virtual_surface, current_size)
    window.blit(scaled_surface, (0, 0))

    display.update()
    clock.tick(fps)





















