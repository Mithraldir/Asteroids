from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from circleshape import *

import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    # Create sprite groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set container references
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)  # Add comma to make it a tuple!

    # Create game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    print("Starting Asteroids!")

    # Main game loop
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        keys = pygame.key.get_pressed()
        screen.fill("black")

        # Update all objects
        updatable.update(dt)
        shots.update(dt)
        Player.timer -= dt
        # Check for collisions between player and asteroids
        if keys[pygame.K_SPACE]:
            if Player.timer <= 0:  # Only shoot if timer allows it
                shot = player.shoot()  # Create the shot
                if shot:  # If shot was successfully created
                    shots.add(shot)
                    Player.timer = PLAYER_SHOOT_COOLDOWN  # Reset timer to cooldown value

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                exit()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    asteroid.split()
                    shot.kill()


        # Draw all drawable objects
        for sprite in drawable:
            sprite.draw(screen)
        for shot in shots:
            shot.draw(screen)

        pygame.display.flip()

        # Lock framerate and calculate delta time
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
