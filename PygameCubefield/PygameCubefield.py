import pygame
import random
import pygame.font

pygame.init()

  
canvas = pygame.display.set_mode((800, 800))
pygame.display.set_caption("CubeField")
font = pygame.font.Font(None, 50)
def main():
    canvas.fill((255,255,255))
    popup_surface = pygame.Surface((400, 200))
    popup_surface.fill((255, 255, 255))  # White background
    popup_text1 = font.render("Welcome to Cubefield!", True, (0, 0, 0))
    popup_text2 = font.render("Use A and D to move!", True, (0, 0, 0))
    popup_text3 = font.render("Press any key to start!", True, (0,0,0))

    popup_text_rect1 = popup_text1.get_rect()
    popup_text_rect1.center = (popup_surface.get_width() // 2, popup_surface.get_height() // 2 - 40)
    popup_text_rect2 = popup_text2.get_rect()
    popup_text_rect2.center = (popup_surface.get_width() // 2, popup_surface.get_height() // 2)
    popup_text_rect3 = popup_text3.get_rect()
    popup_text_rect3.center = (popup_surface.get_width() // 2, popup_surface.get_height() // 2 + 40)

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
    pause = True
    while pause:
        for event in pygame.event.get():
            if event.type == 
            if event.type == pygame.MOUSEBUTTONUP:
                pause = False
    main()



if __name__ == "__main__":
    main()
