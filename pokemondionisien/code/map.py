import pytmx
import pyscroll
import pygame

from screen import Screen
from switch import Switch
class Map:
    def __init__(self, screen: Screen):
        self.screen = screen
        self.tmx_data = None
        self.map_layer = None
        self.groupe = None
        self.player = None
        self.switch: list[Switch] = []

        self.switch_map("map_start")
    def switch_map(self, map: str):
        self.tmx_data = pytmx.load_pygame(f"../assets/map/{map}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=7)

        self.switch = []
        for obj in self.tmx_data.objects :
            type_obj = obj.name.split(' ')[0]
            name_obj = obj.name.split(' ')[1]
            port_obj = obj.name.split(' ')[-1]
            if type_obj == "switch":
                self.switch.append(Switch(
                    type_obj, 
                    name_obj, 
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height), 
                    port_obj
                ))
        
        # for elem in self.switch:
        #     print(elem.name)
    def update(self):
        self.group.update()
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

    def add_player(self, player):
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switch(self.switch)