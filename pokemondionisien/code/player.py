import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from pokemon import Pokemon
from switch import Switch

class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.pokedollars: int = 0
        self.pokemons = [Pokemon.create_pokemon("Pikachu", 10),
                         Pokemon.create_pokemon("Charizard", 10),
                         Pokemon.create_pokemon("Squirtle", 10)]
        self.switch: list[Switch] = []
        self.collisions = []
        self.change_map: Switch = None

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.animation_walk is False:
            next_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                next_hitbox = self.check_hitbox("left", next_hitbox)
                if not self.check_collision(next_hitbox):
                    
                    self.check_collisions_switch(next_hitbox)
                    self.move_left()
                else:
                    self.direction = "left"
            elif self.keylistener.key_pressed(pygame.K_d):
                next_hitbox = self.check_hitbox("right", next_hitbox)
                if not self.check_collision(next_hitbox):

                    self.check_collisions_switch(next_hitbox)
                    self.move_right()
                else:
                    self.direction = "right"
            elif self.keylistener.key_pressed(pygame.K_z):
                next_hitbox = self.check_hitbox("up", next_hitbox)
                if not self.check_collision(next_hitbox):

                    self.check_collisions_switch(next_hitbox)
                    self.move_up()
                else:
                    self.direction = "up"
            elif self.keylistener.key_pressed(pygame.K_s):
                next_hitbox = self.check_hitbox("down", next_hitbox)
                if not self.check_collision(next_hitbox):

                    self.check_collisions_switch(next_hitbox)
                    self.move_down()
                else:
                    self.direction = "down"

            elif self.keylistener.key_pressed(pygame.K_m):
                self.get_position()
    
    def check_hitbox(self, direction: str, next_hitbox):
        if direction == "left":
            next_hitbox.x -= 16
        elif direction == "right":
            next_hitbox.x += 16
        elif direction == "up":
            next_hitbox.y -= 16
        elif direction == "down":
            next_hitbox.y += 16
        return next_hitbox
    
    def check_collisions_switch(self, next_hitbox: pygame.Rect):
        if self.switch:
            for switch in self.switch:
                if switch.check_collision(next_hitbox):
                    print("collision")
                    print("switch_player", switch.name)
                    self.change_map = switch
                return None
            
    def check_collision(self, hitbox: pygame.Rect) -> bool:
        for collision in self.collisions:
            if hitbox.colliderect(collision):
                return True
        return None

    def add_switch(self, switch: Switch):
        self.switch = switch

    def add_collisions(self, collisions):
        self.collisions = collisions