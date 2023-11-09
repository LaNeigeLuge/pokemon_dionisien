import pygame
from keylistener import KeyListener
from map import Map
from player import Player
from screen import Screen
from menu import Menu


class Game:
    def __init__(self):
        self.running: bool = True
        self.paused: bool = False
        self.menu: Menu = Menu()
        self.screen: Screen = Screen()
        self.map: Map = Map(self.screen)
        self.keylistener: KeyListener = KeyListener()
        self.player: Player = Player(self.keylistener, self.screen, 406, 201)
        self.map.add_player(self.player)

    def run(self) -> None:
        while self.running:
            self.handle_input()
            if self.paused is True:
                self.map.update()
                self.menu.display()
                self.paused = self.menu.paused
            else:
                self.map.update()

            self.screen.update()

    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                self.keylistener.add_key(event.key)
                if event.key == pygame.K_SPACE:
                    print("Pausing game")
                    self.paused = self.paused is not True
                    self.menu.paused = self.paused
            elif event.type == pygame.KEYUP:
                self.keylistener.remove_key(event.key)
            