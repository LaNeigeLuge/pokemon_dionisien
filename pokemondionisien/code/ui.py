import pygame
from screen import Screen
from pokemon import Pokemon

screen = Screen()

class Button(pygame.sprite.Sprite):
    def __init__(self, pos = (0,0), text: str = "Click", fontsize = 16, colors: dict = None, hover_colors: dict = None, command: callable = None,): 
        if command is None:
            command = lambda: print("No command assigned to this button")
        if colors is None:
            colors = {"foreground": (255, 255, 255), "background": (0, 0, 0)}
        if hover_colors is None:
            hover_colors = {"foreground": (0, 0, 0), "background": (255, 255, 255)}
    
        super().__init__()

        # Screen
        self.screen = Screen()
        self.screen_display = self.screen.get_display()

        # Button Properties
        self.pos = pos
        self.text = text
        self.font = pygame.font.SysFont("Arial", fontsize)
        
        # Colors
        self.foreground_color = colors["foreground"]
        self.background_color = colors["background"]
        self.hover_foreground_color = hover_colors["foreground"]
        self.hover_background_color = hover_colors["background"]

        # Button Action
        self.command = command

        self.create_button()
        self.create_hover_button()

    def create_button(self):
        self.image = self.create_image(self.text, self.foreground_color, self.background_color)
        self.original_image = self.image.copy()

    def create_hover_button(self):
        self.hover_image = self.create_image(self.text, self.hover_foreground_color, self.hover_background_color)
        self.pressed = 1

    def create_image(self, text, foreground_color, background_color):
        self.text = text
        image = self.font.render(self.text, 1, foreground_color)
        self.rect = image.get_rect()
        self.rect.x, self.rect.y = self.pos
        button_surface = pygame.Surface((self.rect.width, self.rect.height))
        button_surface.fill(background_color)
        button_surface.blit(image, (0, 0))
        return button_surface

    def update(self):
        # Check if button is hovered on or clicked
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.image = self.hover_image
            self.check_click()
        else:
            self.image = self.original_image

    def check_click(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0] and self.pressed == 1:
                self.command()
                self.pressed = 0
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.pressed = 1
 
class PokemonBox(pygame.sprite.Sprite):
    def __init__(self, pokemon: Pokemon, pos = (0,0), fontsize = 16, colors: dict = None):
        super().__init__()
                
        # Box Properties
        self.pos = pos
        pokemon_move_names = [move.dbSymbol for move in pokemon.moves]
        self.text = f"Name: {pokemon.dbSymbol} - Level: {pokemon.level} - Type: {pokemon.type}\n \
                    HP: {pokemon.hp} - Speed: {pokemon.spd}\n \
                    Attack: {pokemon.atk} - Defense: {pokemon.dfe}\n \
                    Special Attack: {pokemon.ats} - Special Defense: {pokemon.dfs}\n \
                    Moveset: {pokemon_move_names} \
                    "

        self.fontsize = fontsize
        self.font = pygame.font.SysFont("Arial", self.fontsize)

        # Colors
        self.foreground_color = colors["foreground"]
        self.background_color = colors["background"]

        # Line Spacing
        self.spacing = 5

        self.create_box()

    def create_box(self):
        self.image = self.create_image()
        self.original_image = self.image.copy()
    
    def create_image(self):
        rendered_text, rect = self.create_multiline_text()

        self.rect = rect
        self.rect.x, self.rect.y = self.pos
        print(self.rect)
        box_surface = pygame.Surface((self.rect.width, self.rect.height))
        box_surface.fill(self.background_color)

        for image, rect in rendered_text:
            print(f"rect: {rect}")
            box_surface.blit(image, rect)
        return box_surface
    
    def update(self):
        self.image = self.original_image

    def create_multiline_text(self):
        rendered_text = []
        box_width = 0
        box_height = 0
        for i, line in enumerate(self.text.split('\n')):
            line_image = self.font.render(line, 1, self.foreground_color)
            line_rect = line_image.get_rect()
            line_rect.topleft = (0, (self.spacing + self.fontsize)* i)

            if line_rect.width > box_width:
                box_width = line_rect.width
            
            box_height += self.spacing + self.fontsize
            print(f"box width: {box_width}, box height: {box_height}")
            print("line rect: ", line_rect)
            rendered_text.append((line_image, line_rect))
        
        rect = pygame.Rect(0, 0, box_width, box_height)
        return rendered_text, rect