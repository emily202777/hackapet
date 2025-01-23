# import libraries
import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label
import random

import math

# initalize
pygame.init()
display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)
# display living room background
room_background = displayio.OnDiskBitmap("livingRoomBackground.bmp")
bg_sprite = displayio.TileGrid(room_background, pixel_shader=room_background.pixel_shader)
splash.append(bg_sprite)
# add pet sprite
# NEED TO CHANGE/MAKE SURE FULLY CUSTOMIZED
# Load the pet sprite sheet (idleRabbi.bmp)
rabbi_sheet = displayio.OnDiskBitmap("/pets/rabbi/idleRabbi.bmp")

tile_width = 64
tile_height = 64
rabbi_sprite = displayio.TileGrid(
    rabbi_sheet,
    pixel_shader=rabbi_sheet.pixel_shader,
    width=1,  # 1 tile wide
    height=1,  # 1 tile tall
    tile_width=tile_width,
    tile_height=tile_height,
    default_tile=0,  # first frame of animation
    x=(display.width - tile_width) // 2,  # horizontally centered
    y=display.height - tile_height - 10  # near bottom of screen
)

splash.append(rabbi_sprite)  # Add sprite to the splash (display) group

# food collecting game (big chungus)
# load food animations - got rid of water sheet, just cookie & carrot collecting, will use water bowl differently
carrot_sheet = displayio.OnDiskBitmap("/pets/rabbi/bouncingCarrot.bmp")
cookie_sheet = displayio.OnDiskBitmap("/pets/rabbi/bouncingCookie.bmp")
# empty list for food properties
def spawn_food():
    food_type = random.choice([carrot_sheet, cookie_sheet])
    x_position = random.randint(0, display.width - 16)
    food = displayio.TileGrid(
        food_type,
        pixel_shader=food_type.pixel_shader,
        width=1,
        height=1,
        tile_width=16,
        tile_height=16,
        x=x_position,
        y=-32  # starts above screen
    )
    
    food.frame = 0  # initial food frame
    food.frame_count = 12 if food_type == carrot_sheet else 23  # 12 frames for carrot, 23 for cookie
    food.frame_rate = 0.1  # Time delay between each frame update (adjust for smoother animation)
    food_items.append(food)
    splash.append(food)

# collision check function
def check_collision(sprite1, sprite2):
    return (
        sprite1.x < sprite2.x + 16 and
        sprite1.x + 16 > sprite2.x and
        sprite1.y < sprite2.y + 16 and
        sprite1.y + 16 > sprite2.y
    )
# score count
score = 0
font = terminalio.FONT  # default font
score_label = label.Label(font, text="Score: 0", color=0xFFFFFF)
score_label.x = 10
score_label.y = 10
splash.append(score_label)

frame = 0
speed = 4  # pet movement speed
game_over = False

# bounce vars
bounce_amplitude = 5  # How much the food bounces
bounce_speed = 0.1    # How fast the food bounces

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            pet_sprite.x -= speed
        if keys[pygame.K_RIGHT]:
            pet_sprite.x += speed

        # Randomly spawn food items
        if random.random() < 0.05:  # Adjust spawn rate
            spawn_food()
            
   # move food down, check for collisions
    for food in food_items:
        food.y += 2  # speed food falls down

  # Bounce effect
        food.x += math.sin(pygame.time.get_ticks() * bounce_speed) * bounce_amplitude
      
        # update animation frames for food
        food.frame += food.frame_rate
        if food.frame >= food.frame_count:
            food.frame = 0  # Reset to the first frame after reaching the last frame

 food[0] = int(food.frame)  # set current frame for current food item

if food.y > display.height:
            splash.remove(food)
            food_items.remove(food)
        elif check_collision(pet_sprite, food):
            score += 1  # Increment score
            score_label.text = f"Score: {score}"  # Update score display
            splash.remove(food)
            food_items.remove(food)

    # Animate pet sprite
    pet_sprite[0] = frame
    frame = (frame + 1) % frame_count

    time.sleep(0.1)
