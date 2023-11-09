import pygame
from screen import Screen
from ui import Button, PokemonBox
from player import Player
from keylistener import KeyListener

class Menu:
    def __init__(self) -> None:
        self.screen = Screen()
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 0, 0)
        self.screen_display = self.screen.get_display()
        self.surface = pygame.Surface((1080, 520), flags=pygame.SRCALPHA)
        self.background_rect = pygame.Rect(0, 0, 1080, 520)
        self.background_color = (0, 0, 0, 200)

        self.paused = True

        # Menu Items
        self.ui_elements = pygame.sprite.Group()
        self.create_menu_buttons()
        self.create_pokemon_boxes()


    def create_menu_buttons(self):
        button_colors = {"foreground": (255, 255, 255), "background": (0, 0, 0)}
        hover_button_colors = {"foreground": (0, 0, 0), "background": (255, 255, 255)}

        resume_command = lambda: self.resume_game()
        resume_button = Button((150, 150), "Resume", 20, button_colors, hover_button_colors, resume_command)

        quit_command = lambda: pygame.quit()
        quit_button = Button((150, 200), "Quit", 20, button_colors, hover_button_colors, quit_command)

        self.ui_elements.add(resume_button)
        self.ui_elements.add(quit_button)

    def create_pokemon_boxes(self):
        pokemon_pos = (250, 150)
        for pokemon in self.player.pokemons:
            pokemon_box = PokemonBox(pokemon, pokemon_pos, 20, {"foreground": (255, 255, 255), "background": (0, 0, 0)})
            self.ui_elements.add(pokemon_box)
            pokemon_pos = (pokemon_pos[0], pokemon_pos[1] + pokemon_box.rect.height)

    def display(self) -> None:
        pygame.draw.rect(self.surface, self.background_color, self.background_rect)
        self.screen_display.blit(self.surface, (100,100))
        self.ui_elements.update()
        self.ui_elements.draw(self.screen_display)
    
    def resume_game(self) -> None:
        self.paused = False
        print("Resuming game")