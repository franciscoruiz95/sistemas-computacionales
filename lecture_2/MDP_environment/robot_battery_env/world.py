import pygame

from . import settings
from .tilemap import TileMap

class World:
    def __init__(self, title, state, action, initial_energy):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        
        pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_robot = True
        self.render_battery = True
        self.tilemap = None
        self.finish_state = None
        self.initial_energy = initial_energy 
        self.current_energy = initial_energy
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = ["tile" for _ in range(settings.NUM_TILES)]
        for _, actions_table in settings.P.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated and reward > 0:
                            self.finish_state = state

        tile_texture_names[self.finish_state] = "tile"
        self.tilemap = TileMap(tile_texture_names)
    
    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_robot = True
        self.render_battery = True

    def update(self, state, action, reward, terminated, energy):
        if terminated and state == self.finish_state:
            self.render_battery = False
            settings.SOUNDS['win'].play()

        self.current_energy = energy
        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        if self.current_energy > 0.5*self.initial_energy or not self.render_battery:
            self.render_surface.blit(settings.TEXTURES['level_full_battery'], (settings.WINDOW_WIDTH/2, 0))
        elif self.current_energy > 0.1*self.initial_energy and self.current_energy <= 0.5*self.initial_energy:
            self.render_surface.blit(settings.TEXTURES['level_mid_battery'], (settings.WINDOW_WIDTH/2, 0))
        else:
            self.render_surface.blit(settings.TEXTURES['level_low_battery'], (settings.WINDOW_WIDTH/2, 0))
            settings.SOUNDS['low_battery'].play()
        
        if not self.render_battery:
            self.current_energy = self.initial_energy
            self.render_surface.blit(
                settings.TEXTURES['win'],
                ((settings.WINDOW_WIDTH - settings.WIN_WIDTH)//2, (settings.WINDOW_HEIGHT - settings.WIN_HEIGHT)//2)
            )
        
        if self.current_energy < 0:
            self.render_surface.blit(
                settings.TEXTURES['game_over'],
                ((settings.WINDOW_WIDTH - settings.GAME_OVER_WIDTH)//2, (settings.WINDOW_HEIGHT - settings.GAME_OVE_HEIGHT)//2)
            )
            pygame.mixer.music.stop()
            settings.SOUNDS['over'].play()

        text_obj = settings.FONTS['font'].render(f"{int(self.current_energy)} %", False, (246, 0, 139))
        text_rect = text_obj.get_rect()
        text_rect.center = (settings.VIRTUAL_WIDTH/2 + 32, 50)
        self.render_surface.blit(text_obj, text_rect)

        if self.render_battery:
            self.render_surface.blit(
                settings.TEXTURES['battery'],
                (self.tilemap.tiles[self.finish_state].x,
                self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_robot:
            self.render_surface.blit(
                settings.TEXTURES['robot'],
                (self.tilemap.tiles[self.state].x,
                self.tilemap.tiles[self.state].y)
            )
            #settings.SOUNDS['step'].play()

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()
    
    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
