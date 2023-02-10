import pygame

from . import settings
from .tilemap import TileMap

class World:
    def __init__(self, title, state, action):
        pygame.init()
        pygame.display.init()
        #pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
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
        self.render_character = True
        self.render_goal = True

    def update(self, state, action, reward, terminated):
        if terminated and state == self.finish_state:
            self.render_goal = False
            #settings.SOUNDS['win'].play()

        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES['battery'],
                (self.tilemap.tiles[self.finish_state].x,
                self.tilemap.tiles[self.finish_state].y)
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES['robot'],
                (self.tilemap.tiles[self.state].x,
                self.tilemap.tiles[self.state].y)
            )

        self.screen.blit(
            pygame.transform.scale(
                self.render_surface,
                self.screen.get_size()),
            (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()
    
    def close(self):
        # pygame.mixer.music.stop()
        # pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
