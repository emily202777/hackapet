# Verify frame count when updating animation frames
def update_food_frame(food):
    food.frame += food.frame_rate
    if food.frame >= food.frame_count:  # Ensure it wraps around correctly
        food.frame = 0  # Reset to the first frame
    food[0] = int(food.frame)  # Set the current frame for the food item

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT]:
            rabbi_sprite.x = max(0, rabbi_sprite.x - speed)  # Prevent moving out of bounds
        if keys[pygame.K_RIGHT]:
            rabbi_sprite.x = min(display.width - tile_width, rabbi_sprite.x + speed)

        # Randomly spawn food items
        if random.random() < 0.05:  # Adjust spawn rate
            spawn_food()

    # Move food down and check for collisions
    for food in food_items[:]:  # Use a copy of the list to avoid modification issues
        food.y += 2  # Speed food falls down

        # Bounce effect
        food.x = min(max(0, food.x + math.sin(pygame.time.get_ticks() * bounce_speed) * bounce_amplitude), display.width - 16)

        # Update animation frames for food
        update_food_frame(food)

        # Remove food if it falls off-screen or collides with the pet
        if food.y > display.height:
            splash.remove(food)
            food_items.remove(food)
        elif check_collision(rabbi_sprite, food):
            score += 1
            score_label.text = f"Score: {score}"  # Update score display
            splash.remove(food)
            food_items.remove(food)

    # Animate pet sprite
    frame = (frame + 1) % frame_count
    rabbi_sprite[0] = frame

    time.sleep(0.1)
