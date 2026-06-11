import math
import random
import sys

import pygame
import pygame.font

pygame.init()

window_size = 800
canvas = pygame.display.set_mode((window_size, window_size * 0.75))
pygame.display.set_caption("CubeField")
font = pygame.font.Font(None, 50)

# we iterate over the colours for changing levels so a global list is helpful
colourList = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]


def main():
    # Title screen
    canvas.fill((255, 255, 255))
    play_popup()

    currentLevel = 0
    currentScore = 0

    # This is the horizon and origin of each square. This puts it about a 3rd of the way into the screen.
    squareOrigin = 0.25 * window_size

    running = True

    highScore = 0

    cubeList = []
    # Configuration to control inital square size. Maybe tweak later?
    squareSize = 30

    # Counters
    # spawnTimer exists to ensure we do not add squares every frame, maybe a better way?
    spawnTimer = 0
    # This currently just spins the spaceship a little
    # Will keep track of rotation in the screen too, but may be out of scope for now
    tilt = 0

    # Current direction and magnitude of movement (-) means squares are moving right to create the appearance of left motion
    # and vice versa
    # Maybe unnecessary, but I like it taking just a little to ramp up.
    movement = 0
    while running:
        # Clear canvas before rendering each frame
        pygame.draw.rect(canvas, (255, 255, 255), (0, 0, window_size, window_size))
        #
        # # Create Horizon line, aiding 3d effect
        pygame.draw.line(canvas, (0, 0, 0), (0, squareOrigin), (1000, squareOrigin), 5)

        # testRays(squareOrigin)
        #
        # useful to keep track of, may serve more purpose than killing momentum down the track
        isMoving = False

        # allow user to quit easier
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

        # This allows for constant detection of a held key.
        # Pygame returns a dictionary keyed by the key names with a true or false value
        keys = pygame.key.get_pressed()

        # allowing us to check if a key is held or not
        # Allows use of arrow and A and D
        # Left percieved motion
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            # movement is negative
            if movement >= 0:
                movement = -0.002
            if movement > -0.005:
                movement *= 1.1
            if tilt > -0.1:
                tilt -= 0.01
            # keep track of if we moved this frame
            isMoving = True

        # right percieved motion.
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            # movement is positive
            if movement <= 0:
                movement = 0.002
            if movement < 0.005:
                movement *= 1.1
            if tilt < 0.1:
                tilt += 0.01

            isMoving = True

        # if no motion this frame, we zero movement and start counteracting tilt
        if not isMoving:
            movement = 0

            if tilt > 0.05:
                tilt -= 0.05
            elif tilt < -0.05:
                tilt += 0.05
            else:
                tilt = 0
        # Move the cubes in the opposite direction to the ship movement, creating the illusion of movement
        # Apply motion to each existing cube
        for cube in cubeList:
            cube.ship_move(-movement)

        # about every 30s new level
        # Detects when the level should change
        if currentScore > 0 and currentScore % 2000 == 0:
            currentLevel += 1
            spawnTimer = 0  # ensure we do not miss a cycle

        z_modifier = 2  # in order to try to get the most optimal gameplay, I can finetune the speed curve with this. Higher means slower to get started

        # 4 times every second, spawn 1-5 cubes. Increase with level, dividing tries to keep the amount of squares
        # the player must deal with somewhat even across each level
        if spawnTimer == 30 // (currentLevel + 3):
            # If it is time for a new level, we create a pathway for 200 score increments, before the speed increase
            if currentScore % 2000 > 1800:
                cubeList.extend(
                    newLevel(squareSize, currentLevel, squareOrigin, z_modifier)
                )
            else:
                cubeList.extend(
                    spawnCubes(squareSize, currentLevel, squareOrigin, z_modifier)
                )
            spawnTimer = 0

        playerRect = pygame.Rect(window_size // 2 - 30, window_size * 0.75 - 60, 60, 60)
        # # UNCOMMMENT TO SHOW HITBOXES
        # pygame.draw.rect(canvas, (255, 0, 0), playerRect, 2)

        # iterating backwards means that front squares are on top and allows us to delete inline
        # This code moves the cubes forwards and deletes those we have passed.
        for i in range(len(cubeList) - 1, -1, -1):
            # Move each cube forward by the exponential series that controls them.
            cubeList[i].move(currentLevel)
            # Detect player collision and gameover if so
            # The value was chosen from what feels fair, may be subject to change
            if cubeList[i].z > 0.4 * z_modifier:
                if cubeList[i].rect.colliderect(playerRect):
                    game_over(currentScore, highScore)
            if cubeList[i].z > 0.5 * z_modifier:
                cubeList.pop(i)

        spawnTimer += 1
        currentScore += 1
        if currentScore > highScore:
            highScore = currentScore

        currentScoreText = font.render(
            "Current Score: " + str(currentScore), True, (0, 0, 0)
        )
        canvas.blit(currentScoreText, (10, 60))

        draw_ship(tilt)

        pygame.display.update()
        pygame.time.Clock().tick(60)


def game_over(score, highScore):
    game_over_text = font.render("Game Over!", True, (0, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {highScore}", True, (0, 0, 0))
    text3 = font.render("Press Enter to try again!", True, (0, 0, 0))

    game_over_rect = game_over_text.get_rect(
        center=(window_size // 2, window_size // 2 - 40)
    )
    score_rect = score_text.get_rect(center=(window_size // 2, window_size // 2))
    high_score_rect = high_score_text.get_rect(
        center=(window_size // 2, window_size // 2 + 40)
    )
    text3_rect = text3.get_rect(center=(window_size // 2, window_size // 2 + 80))

    canvas.blit(game_over_text, game_over_rect)
    canvas.blit(score_text, score_rect)
    canvas.blit(high_score_text, high_score_rect)
    canvas.blit(text3, text3_rect)

    pygame.display.update()
    pygame.time.wait(1000)  # Pause for a second to stop accidentally retrying.
    pause()
    main()


def spawnCubes(squareSize, currentLevel, squareOrigin, z_modifier):
    cubeList = []
    for i in range(random.randint(1, 5)):
        cubeList.append(
            Cube(
                random.random(),  # Random x position from 0 to 1
                0.05,  # start at 0 z
                squareSize,  # starting size of sqaure, scales in class as moves
                colourList[currentLevel % len(colourList)],  # change colours with level
                squareOrigin - 1.5 * squareSize,  # start slightly above horizon
                z_modifier,
            ),
        )
    return cubeList


def newLevel(squareSize, currentLevel, squareOrigin, z_modifier):
    cubeList = []
    for i in range(2):
        cubeList.append(
            Cube(
                (0.6 - 0.2 * i)
                - squareSize
                / window_size
                / 2,  # This makes 2 rows, centred around the window. Moves with player
                0.05,  # start at 0 z
                squareSize,  # starting size of sqaure, scales in class as moves
                colourList[currentLevel % len(colourList)],  # change colours with level
                squareOrigin - 1.5 * squareSize,  # start above horizon
                z_modifier,
            ),
        )
    return cubeList


def draw_ship(tilt):
    ship_x = window_size / 2
    ship_y = window_size * 0.75 - 40

    # Calculate rotation based on tilt
    angle = tilt * 1.5
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    def rot(px, py):
        rx = px * cos_a - py * sin_a
        ry = px * sin_a + py * cos_a
        return (ship_x + rx, ship_y + ry)

    # Outer Chevron (Dark Grey)
    pygame.draw.polygon(
        canvas, (100, 100, 100), [rot(0, -50), rot(-50, 30), rot(-30, 30), rot(0, -20)]
    )
    pygame.draw.polygon(
        canvas, (80, 80, 80), [rot(0, -50), rot(50, 30), rot(30, 30), rot(0, -20)]
    )

    # Inner Chevron (Orange)
    pygame.draw.polygon(
        canvas, (255, 150, 0), [rot(0, -30), rot(-35, 20), rot(-20, 20), rot(0, -5)]
    )
    pygame.draw.polygon(
        canvas, (200, 100, 0), [rot(0, -30), rot(35, 20), rot(20, 20), rot(0, -5)]
    )


class Cube:
    def __init__(self, x, z, cube_size, cube_color, squareOrigin, z_modifier):
        self.x = x
        self.z = z
        self.cube_size = cube_size
        self.cube_color = cube_color
        self.squareOrigin = squareOrigin
        self.z_modifier = z_modifier

    def move(self, level):
        # Move the cube towards the player by increasing z value
        self.z *= (
            1.03 + 0.01 * level
        )  # Adjust this value to control the speed of the cube. CURRENT: 1 unit per 5000 frames (5 seconds at 60 FPS)
        # z does not increase linearly however, as the cube gets closer it moves faster, this is because of the perspective maths in draw_cube

        self.draw_cube(self.x, self.z, self.cube_size, self.cube_color)

    def ship_move(self, movement):
        self.x += movement

    def draw_cube(self, x, z, cube_size, cube_color):
        z = z / self.z_modifier
        offset, perspectiveSize = self.calculate_perspective(x, z, cube_size)

        self.rect = pygame.Rect(
            (x + offset) * window_size,
            z * window_size + self.squareOrigin,
            perspectiveSize,
            perspectiveSize,
        )
        pygame.draw.rect(
            canvas,
            cube_color,
            self.rect,
        )
        pygame.draw.rect(
            canvas,
            (0, 0, 0),
            self.rect,
            2,
        )

        # # developer tool to display current z - value on each square
        #
        # currentScoreText = font.render(str(round(z, 2)), True, (0, 0, 0))
        # canvas.blit(
        #     currentScoreText,
        #     ((x + offset) * window_size, z * window_size + self.squareOrigin),
        # )

    def calculate_perspective(self, x, z, cube_size):
        # Exaggerate the difference in x, by the same amount we are increasing size.
        angle = (x - 0.5) * 7

        # Use the cos value to interpolate an offset for the x value. Z is how far the cube has travelled towards the player.
        offset = (angle) * z

        # calculate perspective size -> inversely proportional to distance from viewer
        perspectiveSize = cube_size * (1 + z * 7)
        return offset, perspectiveSize


# def testRays(squareOrigin):
#     randLoc = random.random()
#     angle = math.cos(randLoc * (math.pi)) * 2
#     print(angle)
#     # draw ray
#     pygame.draw.line(
#         canvas,
#         (0, 0, 0),
#         (randLoc * window_size, squareOrigin),
#         ((randLoc - angle) * window_size, window_size),
#     )


def play_popup():
    popup_surface = pygame.Surface((400, 200))
    popup_surface.fill((255, 255, 255))  # White background
    popup_text1 = font.render("Welcome to Cubefield!", True, (0, 0, 0))
    popup_text2 = font.render("Use A and D to move!", True, (0, 0, 0))
    popup_text3 = font.render("Press Enter to start!", True, (0, 0, 0))

    popup_text_rect1 = popup_text1.get_rect()
    popup_text_rect1.center = (
        popup_surface.get_width() // 2,
        popup_surface.get_height() // 2 - 40,
    )
    popup_text_rect2 = popup_text2.get_rect()
    popup_text_rect2.center = (
        popup_surface.get_width() // 2,
        popup_surface.get_height() // 2,
    )
    popup_text_rect3 = popup_text3.get_rect()
    popup_text_rect3.center = (
        popup_surface.get_width() // 2,
        popup_surface.get_height() // 2 + 40,
    )

    # Draw the text onto the pop-up surface
    popup_surface.blit(popup_text1, popup_text_rect1)
    popup_surface.blit(popup_text2, popup_text_rect2)
    popup_surface.blit(popup_text3, popup_text_rect3)

    # Calculate the center coordinates for the pop-up on the screen
    screen_center_x = canvas.get_width() // 2
    screen_center_y = canvas.get_height() // 2
    popup_rect = popup_surface.get_rect()
    popup_rect.center = (screen_center_x, screen_center_y)

    # Blit the pop-up surface onto the main canvas
    canvas.blit(popup_surface, popup_rect)

    # Update the display to show the pop-up
    pygame.display.update()
    pause()


def pause():
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    pause = False
                    canvas.fill((255, 255, 255))


if __name__ == "__main__":
    main()
