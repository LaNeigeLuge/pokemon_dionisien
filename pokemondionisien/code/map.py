import pytmx
import pyscroll
import pygame

from screen import Screen
from switch import Switch
from player import Player
class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.groupe = None
        self.player = None
        self.switch: list[Switch] = []
        self.collisions = []

        self.current_map: Switch = Switch("switch", "map_start", pygame.Rect(0, 0, 0, 0), 0)
        self.switch_map(self.current_map)

    def switch_map(self, switch: Switch):
        print(" current map",self.current_map.name)
        self.tmx_data = pytmx.load_pygame(f"./assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)

        if switch.name.split(" ")[0] == switch.name:
            self.map_layer.zoom = 2
        else:
            self.map_layer.zoom = 3.75

        self.switch = []
        self.collisions = []


        print(self.tmx_data.objects)
        for obj in self.tmx_data.objects :
            print("obj.name : ", obj.name)
            if obj.name == "collision":
                self.collisions.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            elif obj.name.split(' ')[0] == "switch":
                type_obj = obj.name.split(' ')[0]
                name_obj = obj.name.split(' ')[1]
                port_obj = obj.name.split(' ')[-1]
                self.switch.append(Switch(
                    type_obj, 
                    name_obj, 
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height), 
                    port_obj
                ))
            

        if self.player:
            self.change_position(switch)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switch(self.switch)
            self.player.add_collisions(self.collisions)
            self.group.add(self.player)

        self.current_map = switch


    def update(self):
        if self.player:
            if self.player.change_map and self.player.step >= 8:
                self.switch_map(self.player.change_map)
                self.player.change_map = None

        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def add_player(self, player):
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switch(self.switch)
        self.player.add_collisions(self.collisions)

    def change_position(self, switch):
        print(" le switch est ", switch.name)
        print(" le current map est ", self.current_map.name)

        if switch.name == "map_start":
            position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
            self.player.position = pygame.math.Vector2(position.x, position.y)
        
        else:
            position = self.tmx_data.get_object_by_name("spawn " + switch.name + " " + str(switch.port))
            self.player.position = pygame.math.Vector2(position.x, position.y)