import pygame
from screen import Screen
from ui import Button
from player import Player
from keylistener import KeyListener
import json
import time


class MenuTab:
    """Base class for menu tabs"""
    def __init__(self, screen: Screen, player: Player):
        self.screen = screen
        self.player = player
        self.ui_elements = pygame.sprite.Group()

    def update(self):
        self.ui_elements.update()

    def draw(self, surface):
        self.ui_elements.draw(surface)

    def handle_key(self, key):
        """Handle keyboard input"""
        pass


class PartyTab(MenuTab):
    """Pokemon Party tab - shows your team"""
    def __init__(self, screen: Screen, player: Player):
        super().__init__(screen, player)
        self.create_party_display()

    def create_party_display(self):
        """Display Pokemon party with better formatting"""
        font = pygame.font.SysFont("Arial", 18)
        y_pos = 80

        for i, pokemon in enumerate(self.player.pokemons):
            # Pokemon name and level
            text = f"{i+1}. {pokemon.dbSymbol.upper()} - Lv.{pokemon.level}"
            color = (255, 215, 0) if pokemon.shiny else (255, 255, 255)

            # Create text surface (not a button, just display)
            text_surface = font.render(text, True, color)

            # HP Bar
            hp_percent = pokemon.hp / pokemon.max_hp
            hp_bar_width = 200
            hp_bar_height = 10

            y_pos += 60


class PokedexTab(MenuTab):
    """Pokedex tab - shows caught Pokemon"""
    def __init__(self, screen: Screen, player: Player):
        super().__init__(screen, player)
        self.create_pokedex()

    def create_pokedex(self):
        font = pygame.font.SysFont("Arial", 16)

        if not hasattr(self.player, 'pokedex'):
            self.player.pokedex = set([p.dbSymbol for p in self.player.pokemons])

        text = f"Pokemon Seen: {len(self.player.pokedex)}"
        # Display pokedex info


class BagTab(MenuTab):
    """Bag/Inventory tab"""
    def __init__(self, screen: Screen, player: Player):
        super().__init__(screen, player)

        # Initialize inventory if not exists
        if not hasattr(self.player, 'inventory'):
            self.player.inventory = {
                'pokeballs': 5,
                'potions': 3,
                'super_potions': 1,
                'revives': 2
            }

        self.create_bag_display()

    def create_bag_display(self):
        font = pygame.font.SysFont("Arial", 18)
        y_pos = 80

        for item_name, quantity in self.player.inventory.items():
            item_display = f"{item_name.replace('_', ' ').title()}: x{quantity}"
            # Display item


class PlayerTab(MenuTab):
    """Player info tab"""
    def __init__(self, screen: Screen, player: Player):
        super().__init__(screen, player)

        # Initialize player stats if not exists
        if not hasattr(self.player, 'playtime_start'):
            self.player.playtime_start = time.time()
        if not hasattr(self.player, 'badges'):
            self.player.badges = 0

        self.create_player_display()

    def create_player_display(self):
        """Display player information"""
        pass


class OptionsTab(MenuTab):
    """Settings/Options tab"""
    def __init__(self, screen: Screen, player: Player):
        super().__init__(screen, player)
        self.create_options()

    def create_options(self):
        button_colors = {"foreground": (255, 255, 255), "background": (50, 50, 50)}
        hover_colors = {"foreground": (0, 0, 0), "background": (200, 200, 200)}

        # Save button
        save_btn = Button((150, 150), "Save Game", 20, button_colors, hover_colors,
                         lambda: self.save_game())
        self.ui_elements.add(save_btn)

        # Load button
        load_btn = Button((150, 200), "Load Game", 20, button_colors, hover_colors,
                         lambda: self.load_game())
        self.ui_elements.add(load_btn)

    def save_game(self):
        """Save game to file"""
        save_data = {
            'player_position': (self.player.position.x, self.player.position.y),
            'pokedollars': self.player.pokedollars,
            'pokemons': [],
            'inventory': getattr(self.player, 'inventory', {}),
            'badges': getattr(self.player, 'badges', 0)
        }

        # Save Pokemon data
        for pokemon in self.player.pokemons:
            save_data['pokemons'].append({
                'name': pokemon.dbSymbol,
                'level': pokemon.level,
                'hp': pokemon.hp,
                'xp': pokemon.xp,
                'ivs': pokemon.ivs,
                'moves': [m.dbSymbol for m in pokemon.moves]
            })

        with open('savegame.json', 'w') as f:
            json.dump(save_data, f, indent=2)

        print("✓ Game saved!")

    def load_game(self):
        """Load game from file"""
        try:
            with open('savegame.json', 'r') as f:
                save_data = json.load(f)
            print("✓ Game loaded!")
            # TODO: Actually apply loaded data
        except FileNotFoundError:
            print("✗ No save file found!")


class EnhancedMenu:
    """Enhanced menu system with tabs and keyboard navigation"""

    def __init__(self, player: Player) -> None:
        self.screen = Screen()
        self.player = player
        self.screen_display = self.screen.get_display()

        # Menu state
        self.paused = True
        self.current_tab = 0

        # Tab names
        self.tab_names = ["Party", "Pokedex", "Bag", "Player", "Options"]

        # Colors
        self.bg_color = (20, 20, 40, 220)
        self.tab_bg = (40, 40, 60)
        self.tab_active = (80, 120, 200)
        self.text_color = (255, 255, 255)

        # Fonts
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.tab_font = pygame.font.SysFont("Arial", 18)
        self.text_font = pygame.font.SysFont("Arial", 16)

        # Create menu surface
        self.surface = pygame.Surface((1080, 600), flags=pygame.SRCALPHA)

        # Create tabs
        self.tabs = [
            PartyTab(self.screen, self.player),
            PokedexTab(self.screen, self.player),
            BagTab(self.screen, self.player),
            PlayerTab(self.screen, self.player),
            OptionsTab(self.screen, self.player)
        ]

        # Close button
        self.ui_elements = pygame.sprite.Group()
        button_colors = {"foreground": (255, 255, 255), "background": (180, 50, 50)}
        hover_colors = {"foreground": (255, 255, 255), "background": (220, 80, 80)}

        close_btn = Button((950, 50), "Close [ESC]", 18, button_colors, hover_colors,
                          lambda: self.close_menu())
        self.ui_elements.add(close_btn)

    def handle_key(self, key):
        """Handle keyboard navigation"""
        if key == pygame.K_LEFT:
            self.current_tab = (self.current_tab - 1) % len(self.tabs)
        elif key == pygame.K_RIGHT:
            self.current_tab = (self.current_tab + 1) % len(self.tabs)
        elif key == pygame.K_ESCAPE or key == pygame.K_SPACE:
            self.close_menu()
        else:
            # Pass key to current tab
            self.tabs[self.current_tab].handle_key(key)

    def close_menu(self):
        self.paused = False

    def draw_tabs(self):
        """Draw tab buttons"""
        tab_width = 180
        tab_height = 40
        tab_x = 100
        tab_y = 120

        for i, tab_name in enumerate(self.tab_names):
            # Tab background
            color = self.tab_active if i == self.current_tab else self.tab_bg
            rect = pygame.Rect(tab_x + i * (tab_width + 10), tab_y, tab_width, tab_height)
            pygame.draw.rect(self.surface, color, rect, border_radius=5)

            # Tab text
            text = self.tab_font.render(tab_name, True, self.text_color)
            text_rect = text.get_rect(center=rect.center)
            self.surface.blit(text, text_rect)

    def draw_player_info(self):
        """Draw player info at top"""
        y = 60

        # Player name
        name_text = self.title_font.render("Trainer", True, (255, 215, 0))
        self.surface.blit(name_text, (120, y))

        # Money
        money_text = self.text_font.render(f"${self.player.pokedollars}", True, self.text_color)
        self.surface.blit(money_text, (300, y + 5))

        # Badges
        if hasattr(self.player, 'badges'):
            badges_text = self.text_font.render(f"Badges: {self.player.badges}", True, self.text_color)
            self.surface.blit(badges_text, (450, y + 5))

        # Playtime
        if hasattr(self.player, 'playtime_start'):
            elapsed = int(time.time() - self.player.playtime_start)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            time_text = self.text_font.render(f"Time: {hours:02d}:{minutes:02d}", True, self.text_color)
            self.surface.blit(time_text, (620, y + 5))

    def draw_party_tab(self):
        """Draw Pokemon party"""
        y = 180

        for i, pokemon in enumerate(self.player.pokemons):
            x = 120

            # Pokemon number
            num_text = self.text_font.render(f"#{i+1}", True, (150, 150, 150))
            self.surface.blit(num_text, (x, y))

            # Pokemon name and level
            name_color = (255, 215, 0) if pokemon.shiny else (255, 255, 255)
            name_text = self.title_font.render(f"{pokemon.dbSymbol.upper()}", True, name_color)
            self.surface.blit(name_text, (x + 40, y))

            level_text = self.text_font.render(f"Lv.{pokemon.level}", True, (200, 200, 200))
            self.surface.blit(level_text, (x + 220, y + 5))

            # HP Bar
            hp_bar_x = x + 40
            hp_bar_y = y + 35
            hp_bar_width = 200
            hp_bar_height = 15

            # Background
            pygame.draw.rect(self.surface, (60, 60, 60),
                           (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height), border_radius=3)

            # HP fill
            hp_percent = pokemon.hp / pokemon.max_hp
            fill_width = int(hp_bar_width * hp_percent)

            if hp_percent > 0.5:
                hp_color = (100, 220, 100)
            elif hp_percent > 0.2:
                hp_color = (220, 220, 100)
            else:
                hp_color = (220, 100, 100)

            pygame.draw.rect(self.surface, hp_color,
                           (hp_bar_x, hp_bar_y, fill_width, hp_bar_height), border_radius=3)

            # HP text
            hp_text = self.text_font.render(f"{pokemon.hp}/{pokemon.max_hp}", True, self.text_color)
            self.surface.blit(hp_text, (hp_bar_x + hp_bar_width + 10, hp_bar_y - 2))

            # Types
            type_x = x + 320
            for j, ptype in enumerate(pokemon.type):
                type_text = self.text_font.render(ptype.upper(), True, (255, 255, 255))
                type_bg = pygame.Rect(type_x + j * 80, y + 5, 70, 25)
                pygame.draw.rect(self.surface, (80, 80, 120), type_bg, border_radius=3)
                self.surface.blit(type_text, (type_x + j * 80 + 5, y + 8))

            # Stats (smaller)
            stats_y = y + 35
            stats_x = x + 320
            stats_text = self.text_font.render(
                f"ATK:{pokemon.atk} DEF:{pokemon.dfe} SPD:{pokemon.spd}",
                True, (180, 180, 180)
            )
            self.surface.blit(stats_text, (stats_x, stats_y))

            y += 100

    def draw_bag_tab(self):
        """Draw inventory"""
        y = 180
        x = 150

        title = self.title_font.render("Bag", True, self.text_color)
        self.surface.blit(title, (x, y))
        y += 50

        if hasattr(self.player, 'inventory'):
            for item_name, quantity in self.player.inventory.items():
                item_display = f"{item_name.replace('_', ' ').title()}: x{quantity}"
                text = self.text_font.render(item_display, True, self.text_color)
                self.surface.blit(text, (x + 20, y))
                y += 30
        else:
            empty_text = self.text_font.render("Bag is empty", True, (150, 150, 150))
            self.surface.blit(empty_text, (x + 20, y))

    def draw_pokedex_tab(self):
        """Draw Pokedex"""
        y = 180
        x = 150

        title = self.title_font.render("Pokedex", True, self.text_color)
        self.surface.blit(title, (x, y))
        y += 50

        if not hasattr(self.player, 'pokedex'):
            self.player.pokedex = set([p.dbSymbol for p in self.player.pokemons])

        seen_text = self.text_font.render(f"Pokemon Seen: {len(self.player.pokedex)}", True, self.text_color)
        self.surface.blit(seen_text, (x + 20, y))
        y += 40

        # List caught Pokemon
        for pokemon_name in sorted(self.player.pokedex):
            text = self.text_font.render(f"• {pokemon_name.title()}", True, self.text_color)
            self.surface.blit(text, (x + 20, y))
            y += 25

    def draw_player_tab(self):
        """Draw player stats"""
        y = 180
        x = 150

        title = self.title_font.render("Trainer Card", True, self.text_color)
        self.surface.blit(title, (x, y))
        y += 50

        # Money
        money_text = self.text_font.render(f"Money: ${self.player.pokedollars}", True, self.text_color)
        self.surface.blit(money_text, (x + 20, y))
        y += 35

        # Badges
        badges = getattr(self.player, 'badges', 0)
        badges_text = self.text_font.render(f"Badges: {badges}/8", True, self.text_color)
        self.surface.blit(badges_text, (x + 20, y))
        y += 35

        # Playtime
        if hasattr(self.player, 'playtime_start'):
            elapsed = int(time.time() - self.player.playtime_start)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            time_text = self.text_font.render(f"Play Time: {hours:02d}:{minutes:02d}:{seconds:02d}",
                                             True, self.text_color)
            self.surface.blit(time_text, (x + 20, y))
            y += 35

        # Pokemon count
        pokemon_text = self.text_font.render(f"Pokemon in Party: {len(self.player.pokemons)}",
                                            True, self.text_color)
        self.surface.blit(pokemon_text, (x + 20, y))

    def display(self) -> None:
        """Main display method"""
        # Clear surface
        self.surface.fill(self.bg_color)

        # Draw border
        pygame.draw.rect(self.surface, (100, 100, 150), self.surface.get_rect(), width=3, border_radius=10)

        # Draw player info header
        self.draw_player_info()

        # Draw tabs
        self.draw_tabs()

        # Draw current tab content
        if self.current_tab == 0:  # Party
            self.draw_party_tab()
        elif self.current_tab == 1:  # Pokedex
            self.draw_pokedex_tab()
        elif self.current_tab == 2:  # Bag
            self.draw_bag_tab()
        elif self.current_tab == 3:  # Player
            self.draw_player_tab()
        elif self.current_tab == 4:  # Options
            # Draw options tab content
            pass

        # Draw current tab's UI elements
        self.tabs[self.current_tab].update()
        self.tabs[self.current_tab].draw(self.surface)

        # Blit to screen
        self.screen_display.blit(self.surface, (100, 60))

        # Draw close button
        self.ui_elements.update()
        self.ui_elements.draw(self.screen_display)

        # Draw controls hint
        hint_text = self.text_font.render("← → to switch tabs | ESC to close", True, (200, 200, 200))
        self.screen_display.blit(hint_text, (120, 680))
