import pygame
from os.path import join #this method creates a path with appropriate slashes. 
from random import randint

WINDOW_WIDTH = 1240
WINDOW_HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True 
clock = pygame.time.Clock()

# imports 
player_surf = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surf.get_frect(center=(200,200))

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_coords = [(randint(0,WINDOW_WIDTH),randint(0, WINDOW_HEIGHT)) for _ in range(20)]

meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))

laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20,WINDOW_HEIGHT-20))

#variables
player_direction = pygame.math.Vector2()
player_speed = 400 

# custom events: meteor event 
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

idx = 1
# game loop 
while running:
    dt = clock.tick() / 1000
    #print(dt)
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            print('Meteor Event')
        #if event.type == pygame.KEYDOWN:
        #    print('key pressed')
    
    keys = pygame.key.get_pressed()
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_direction = player_direction.normalize() if player_direction else player_direction
    #print(player_direction)
    player_rect.center += player_direction * player_speed * dt
    if player_rect.bottom >= WINDOW_HEIGHT: player_rect.bottom = WINDOW_HEIGHT
    if player_rect.right >= WINDOW_WIDTH: player_rect.right = WINDOW_WIDTH
    if player_rect.left <= 0: player_rect.left = 0
    if player_rect.top <= 0: player_rect.top = 0

    
    recent_keys = pygame.key.get_just_pressed() 
    # not a perfect solution but better than get_pressed()
    if recent_keys[pygame.K_SPACE]: 
        print('fire laser', idx)
        idx += 1

    # draw the game
    screen.fill('darkslateblue')
    for coord in star_coords:
        screen.blit(star_surf, coord)
    screen.blit(meteor_surf, meteor_rect)
    screen.blit(laser_surf, laser_rect) 

    '''
    if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top <= 0:
         player_direction.y *= -1
    if player_rect.right >= WINDOW_WIDTH or player_rect.left <= 0:
        player_direction.x *= -1
    player_rect.center += player_direction * player_speed * dt
    '''
    screen.blit(player_surf, player_rect)
    # update the frame
    pygame.display.update()
    
pygame.quit()

# Concepts:
# Concept-1: Delta Time 
# Concept-2: Getting input (2 ways)
#   1. Inside the event loop, using event
#   2. Outside the event loop, using pygame.key or pygame.mouse
# Concept-3: Normalizing the player direction vector to keep the speed constant
# Concept-4: Avoiding recognizing key presses on every frame using get_just_pressed() 