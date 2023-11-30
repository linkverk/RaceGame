import pygame
import sys
import subprocess

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Racing Game")

background = pygame.image.load("bg.png")
background = pygame.transform.scale(background, (width, height))

# Set up fonts
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)
option_font = pygame.font.Font(None, 36)  # Using the default font for options

def font(size, path=None):
    return pygame.font.Font(path, size)

# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)

# Initialize variables
start_clicked = False
settings_clicked = False
casual_clicked = False
casual_cpu_clicked = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the user clicked on the "Start" button
            if start_rect.collidepoint(mouse_x, mouse_y):
                start_clicked = True
                settings_clicked = False
                casual_clicked = False
                casual_cpu_clicked = False

            # Check if the user clicked on one of the options
            elif start_clicked:
                options = ["Casual 1 Player VS CPU", "Casual (Player 1 vs Player 2)", "Tournament (4 Players)", "Championship (2 Players)", "Survival (1 Player)"]
                for i, option in enumerate(options):
                    option_rect = option_font.render(option, True, (0, 0, 0)).get_rect(
                        center=(width // 2, height // 4 + (i + 1) * 50)
                    )
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        if "Casual" and "CPU" in option:
                            casual_clicked = True
                            subprocess.run(["python", "casual_file.py"])

    # Draw the background
    screen.blit(background, (0, 0))

    # Render and display "Racing Game" text
    racing_text = font(72, "Race Sport.ttf").render("Racing Game", True, (0, 0, 0))
    racing_rect = racing_text.get_rect(center=(width // 2, height // 6))
    screen.blit(racing_text, racing_rect)

    # Render and display "Settings" text
    settings_text = font(72, "Race Sport.ttf").render("Settings", True, (0, 0, 0))
    settings_rect = settings_text.get_rect(center=(width // 2, height // 2))
    screen.blit(settings_text, settings_rect)

    # Render and display "Start" text
    start_text = font(72, "Race Sport.ttf").render("Start", True, (0, 0, 0))
    start_rect = start_text.get_rect(center=(width // 2, 3 * height // 4))
    screen.blit(start_text, start_rect)

    # Check if "Start" button is clicked
    if start_clicked:
        screen.blit(background, (0, 0))
        options = ["Casual 1 Player VS CPU", "Casual (Player 1 vs Player 2)", "Tournament (4 Players)", "Championship (2 Players)", "Survival (1 Player)"]

        # Render and display options with the default font
        for i, option in enumerate(options):
            option_text = option_font.render(option, True, (0, 0, 0))
            option_rect = option_text.get_rect(center=(width // 2, height // 4 + (i + 1) * 50))
            screen.blit(option_text, option_rect)


    
    if casual_cpu_clicked:
        screen.blit(background, (0, 0))
        subprocess.run(["python", "casual_file.py"])

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
