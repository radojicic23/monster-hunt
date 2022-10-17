import pygame, random

from constants import WINDOW_HEIGHT, WINDOW_WIDTH, display_surface
from monster import MyMonster


FPS = 60

class Game:
    """A class to control gameplay"""
    def __init__(self, player, monster_group):
        """Initialize the game object"""
        # Set game values
        self.score = 0
        self.round_number = 0

        self.round_time = 0
        self.frame_count = 0

        self.player = player
        self.monster_group = monster_group

        # Set sounds and music
        self.next_level_sound = pygame.mixer.Sound("Assets/next_level.wav")

        # Set font
        self.font = pygame.font.Font("Assets/Abrushow.ttf", 24)

        # Set images
        blue_image = pygame.image.load("Assets/blue_monster.png")
        green_image = pygame.image.load("Assets/green_monster.png")
        purple_image = pygame.image.load("Assets/purple_monster.png")
        yellow_image = pygame.image.load("Assets/yellow_monster.png")
        # This list corresponds to the monster_type attribute (# int 0 -> blue, 1 -> green, 2 -> purple, 3 -> yellow)
        self.target_monster_images = [blue_image, green_image, purple_image, yellow_image]

        self.target_monster_type = random.randint(0, 3)
        self.target_monster_image = self.target_monster_images[self.target_monster_type]

        self.target_monster_rect = self.target_monster_image.get_rect()
        self.target_monster_rect.centerx = WINDOW_WIDTH//2
        self.target_monster_rect.top = 30

    def update(self):
        """Update our game object"""
        self.frame_count += 1
        if self.frame_count == FPS:
            self.round_time += 1
            self.frame_count = 0

        # Check for collisions
        self.check_collisions()

    def draw(self):
        """Draw the hud and other to the display"""
        # Set colors
        WHITE = (255, 255, 255)
        BLUE = (20, 176, 235)
        GREEN = (87, 201, 47)
        PURPLE = (226, 73, 243)
        YELLOW = (243, 157, 20)

        # Add the monster colors to a list where the index of the color matches target_monster_images
        colors = [BLUE, GREEN, PURPLE, YELLOW]

        # Set text
        catch_text = self.font.render("Current Catch", True, WHITE)
        catch_rect = catch_text.get_rect()
        catch_rect.centerx = WINDOW_WIDTH//2
        catch_rect.top = 5

        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (5, 35)

        round_text = self.font.render("Current Round: " + str(self.round_number), True, WHITE)
        round_rect = round_text.get_rect()
        round_rect.topleft = (5, 65)

        time_text = self.font.render("Round Time: " + str(self.round_time), True, WHITE)
        time_rect = time_text.get_rect()
        time_rect.topright = (WINDOW_WIDTH - 10, 5)

        warps_text = self.font.render("Warps: " + str(self.player.warps), True, WHITE)
        warps_rect = warps_text.get_rect()
        warps_rect.topright = (WINDOW_WIDTH - 10, 35)

        # Blit the HUD
        display_surface.blit(catch_text, catch_rect)
        display_surface.blit(score_text, score_rect)
        display_surface.blit(round_text, round_rect)
        display_surface.blit(lives_text, lives_rect)
        display_surface.blit(time_text, time_rect)
        display_surface.blit(warps_text, warps_rect)
        display_surface.blit(self.target_monster_image, self.target_monster_rect)

        # Draw a rectangle that is going to be the color of whatever our target monster is
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (WINDOW_WIDTH//2 - 32, 30, 64, 64), 2)
        pygame.draw.rect(display_surface, colors[self.target_monster_type], (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT - 200), 4)

    def check_collisions(self):
        """Check collisions between player and monster"""
        # Check for collision between a player and an individual monster
        collided_monster = pygame.sprite.spritecollideany(self.player, self.monster_group)

        # We collided with a monster
        if collided_monster:
            # Caught the correct monster
            if collided_monster.type == self.target_monster_type:
                self.score += 100 * self.round_number
                # Remove caught monster
                collided_monster.remove(self.monster_group)
                if self.monster_group:  # There are more monsters to catch
                    self.player.catch_sound.play()
                    self.chose_new_target()
                else: # The round is complete
                    self.player.reset()
                    self.start_new_round()
            # Caught the wrong monster
            else:
                self.player.die_sound.play()
                self.player.lives -= 1
                # Check for game over
                if self.player.lives <= 0:
                    self.pause_game("Final Score: " + str(self.score), "Press 'Enter' to play again")
                    self.reset_game()
                self.player.reset()

    def start_new_round(self):
        """Populate with new monsters"""
        # Provide a score bonus based on how quickly the round was finished
        self.score += int(10000 * self.round_number / (1 + self.round_time))

        # Reset round values
        self.round_time = 0
        self.frame_count = 0
        self.round_number += 1
        self.player.warps += 1
        self.player.lives += 1

        # Remove any remaining monsters from a game reset
        for monster in self.monster_group:
            self.monster_group.remove(monster)

        # Add monsters to the monster group
        for _ in range(self.round_number):
            self.monster_group.add(
                MyMonster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[0], 0))
            self.monster_group.add(
                MyMonster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[1], 1))
            self.monster_group.add(
                MyMonster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[2], 2))
            self.monster_group.add(
                MyMonster(random.randint(0, WINDOW_WIDTH - 64), random.randint(100, WINDOW_HEIGHT - 164), self.target_monster_images[3], 3))

        #  Choose a new target monster
        self.chose_new_target()

        self.next_level_sound.play()

    def chose_new_target(self):
        """Chose a new target for the player"""
        target_monster = random.choice(self.monster_group.sprites())
        self.target_monster_type = target_monster.type
        self.target_monster_image = target_monster.image

    def pause_game(self, main_text, sub_text):
        """Pause the game"""
        global running

        # Set color
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)

        # Create the main pause text
        main_text = self.font.render(main_text, True, WHITE)
        main_rect = main_text.get_rect()
        main_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

        # Create the sub pause text
        sub_text = self.font.render(sub_text, True, WHITE)
        sub_rect = sub_text.get_rect()
        sub_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

        # Display the pause text
        display_surface.fill(BLACK)
        display_surface.blit(main_text, main_rect)
        display_surface.blit(sub_text, sub_rect)
        pygame.display.update()

        # Pause the game
        is_paused = True
        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    def reset_game(self):
        """Reset the game"""
        self.score = 0
        self.round_number = 0

        self.player.lives = 5
        self.player.warps = 2
        self.player.reset()

        self.start_new_round()

 