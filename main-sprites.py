#Organizing the game using sprites

from typing import Any
import pygame 
from os.path import join #this method creates a path with appropriate slashes. 
from random import randint, uniform

# CHANGES TO MAKE
#   1. Change score calculating method: Number of meteors hit.
#   2. Change background color to something more realistic.
#   3. After the meteor hits the player three time, game must be over.

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))
        self.direction = pygame.math.Vector2()
        self.speed = 450

        # laser cooldown
        self.can_shoot = True 
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

    def laser_timer(self):
        if not self.can_shoot:
            #print('inside laser timer()')
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * delta_time

        if self.rect.bottom >= WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT
        if self.rect.right >= WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH
        if self.rect.left <= 0: self.rect.left = 0
        if self.rect.top <= 0: self.rect.top = 0

        recent_keys = pygame.key.get_just_pressed() 
        # not a perfect solution but better than get_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot: 
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)
        self.speed = 400
    
    def update(self, delta_time):
        self.rect.centery -= self.speed * delta_time
        if self.rect.bottom < 0: #to remove sprites no longer needed and save up memory
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.original_surf = meteor_surf
        self.image = meteor_surf
        self.rect = self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(-200, -100)))
        self.lifetime = 4000
        self.start_time = pygame.time.get_ticks()
        self.speed = 300
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.rotation_speed = randint(50, 90)
        self.rotation = 0 

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.lifetime:
             self.kill()
        self.rotation += self.rotation_speed * delta_time
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center=self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = pos
    
    def update(self, delta_time):
        self.frame_index += 25 * delta_time
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, star_surf) -> None:
        super().__init__(groups)
        self.image = star_surf
        self.rect = self.image.get_frect(center=(randint(0,WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)))

def check_collisions():
    global running
    if pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask):
        #player.kill()
        #running = False
        print('Meteor hit player')

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)
        if collided_sprites: 
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 1000
    text_surf = font.render(str(current_time), True, 'white')
    text_rect = text_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT - 50))
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, 'white', text_rect.inflate(20,10).move(0, -6), 4, 6)

# general setup
WINDOW_WIDTH = 1240
WINDOW_HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True 
clock = pygame.time.Clock()

# sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
#import only once to avoid 20 imports from within the class
star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha() 
for _ in range(20):
    Star(all_sprites, star_surf)
player = Player(all_sprites)
# stars = [Star(all_sprites) for _ in range(20)]

# imports
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
#meteor_surf = pygame.transform.rotozoom(meteor_surf, 0, 0.75)
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 32)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')) for i in range(21)]

laser_sound = pygame.mixer.Sound(join('audio', 'laser.wav'))
explosion_sound = pygame.mixer.Sound(join('audio', 'explosion.wav'))
game_music = pygame.mixer.Sound(join('audio', 'game_music.wav'))
game_music.set_volume(0.4)
game_music.play(loops=-1)

# custom events: meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

# game loop 
while running:
    dt = clock.tick() / 1000

    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites, meteor_sprites))

    # update
    all_sprites.update(dt)
    check_collisions()
        
    # draw the game
    screen.fill('darkslateblue')
    display_score()
    all_sprites.draw(screen)
    pygame.display.update()
    
pygame.quit()

# Concepts:
# Concept-1: Delta Time 
# Concept-2: Getting input (2 ways)
#   1. Inside the event loop, using event
#   2. Outside the event loop, using pygame.key or pygame.mouse
# Concept-3: Normalizing the player direction vector to keep the speed constant
# Concept-4: Avoiding recognizing key presses on every frame using get_just_pressed() 
# Concept-5: Sprites
#   An in-built class that contains a surface and a rect.
# Concept-6: Displaying sprites
#   Use a pygame sprite group: Groups can draw, update and organize the sprites  
# Concept-7: Working with Time 
#   1. Interval Timer
#   2. Custom Timer 
# Concept-8: Masks
# Concept-9: Rotating objects  