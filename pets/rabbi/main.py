import time
import board
import displayio

# Set up the display
display = board.DISPLAY

# Create a display group
main_group = displayio.Group()

# Load the background image
background = displayio.OnDiskBitmap("/pets/rabbi/livingRoomBackground.bmp")
background_tilegrid = displayio.TileGrid(
    background, pixel_shader=background.pixel_shader
)
main_group.append(background_tilegrid)

# Load the pet's idle animation sprite sheet
pet_idle = displayio.OnDiskBitmap("/pets/rabbi/idleRabbi.bmp")
frame_width = 64  # Width of each frame
frame_height = 64  # Height of each frame
frame_count = 27    # Number of frames in your sprite sheet

# Create a TileGrid for the pet animation
pet_tilegrid = displayio.TileGrid(
    pet_idle,
    pixel_shader=pet_idle.pixel_shader,
    width=1,
    height=1,
    tile_width=frame_width,
    tile_height=frame_height,
    x=32,  # Adjust X position of the pet
    y=32,  # Adjust Y position of the pet
)

main_group.append(pet_tilegrid)

# Show the main group on the display
display.show(main_group)

# Animate the pet
while True:
    for frame in range(frame_count):
        pet_tilegrid[0] = frame  # Update to the current frame
        time.sleep(0.1)         # Pause between frames
