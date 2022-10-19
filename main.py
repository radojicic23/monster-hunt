import pygame 

from monster import MyMonster
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, display_surface
from player import MyPlayer
from game import Game


pygame.init()

# Set FPS
FPS = 60

# Set background image and rect
background_image = pygame.image.load("Assets/background.jpg")
background_rect = background_image.get_rect()
background_rect.topleft = (0, 0)
       
# Create a player group and Player object
my_player_group = pygame.sprite.Group()
my_player = MyPlayer()
my_player_group.add(my_player)

# Create a monster group
my_monster_group = pygame.sprite.Group()
      
# The main game loop
def main():
    # Set clock
    clock = pygame.time.Clock()
    
    running = True
    
    # Create a game object
    my_game = Game(my_player, my_monster_group)
    my_game.pause_game("Monster Hunt", "Press 'Enter' to begin")
    my_game.reset_game()
    
    # Main game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False   
            # Player wants to warp
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    my_player.warp()
    
        # Fill the display
        display_surface.blit(background_image, background_rect)
    
        # Update and draw sprite groups
        my_player_group.update()
        my_player_group.draw(display_surface)
    
        my_monster_group.update()
        my_monster_group.draw(display_surface)
    
        # Update and draw the Game
        my_game.update()
        my_game.draw()
    
        # Update the display and tick clock
        pygame.display.update()
        clock.tick(FPS)
            
    pygame.quit()

main()
