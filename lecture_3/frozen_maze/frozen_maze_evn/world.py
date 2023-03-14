import pygame

from . import settings
from .tilemap import TileMap
from maze_generator.KruskalsMazeGenerator import KruskalsMazeGenerate as Maze
from maze_generator.KruskalsMazeGenerator import E, S


class World:
    def __init__(self, title, state, action):
        pygame.init()
        pygame.display.init()
        pygame.mixer.music.play(loops=-1)
        self.render_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
        )
        self.screen = pygame.display.set_mode(
            (settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title)
        self.current_state = state
        self.current_action = action
        self.render_character = True
        self.render_goal = True
        self.tilemap = None
        self.finish_state = None
        self.maze = Maze(settings.ROWS, settings.COLS)
        self.maze.generate()
        self._create_tilemap()

    def _create_tilemap(self):
        tile_texture_names = ["ice" for _ in range(settings.NUM_TILES)]
        for _, actions_table in settings.P.items():
            for _, possibilities in actions_table.items():
                for _, state, reward, terminated in possibilities:
                    if terminated:
                        if reward > 0:
                            self.finish_state = state
                        else:
                            tile_texture_names[state] = "hole"

        tile_texture_names[self.finish_state] = "ice"

        self.tilemap = TileMap(tile_texture_names)

        i, j = (0, 0)
        for row in self.maze.grid:
            for cell in row:
                state = i * settings.COLS + j
                None if cell & S != 0 \
                    else \
                        self.render_surface.blit(
                            settings.TEXTURES["wall_h"],
                                (self.tilemap.tiles[state].x, self.tilemap.tiles[state].y),
                        )
                if cell & E != 0:
                    None if (cell | row[row.index(cell)+1]) & S != 0 \
                        else \
                            self.render_surface.blit(
                                settings.TEXTURES["wall_h"],
                                    (self.tilemap.tiles[state].x, self.tilemap.tiles[state].y),
                            )
                else:
                    self.render_surface.blit(
                        settings.TEXTURES["wall_v"],
                            (self.tilemap.tiles[state].x, self.tilemap.tiles[state].y),
                    )

                j += 1
            i += 1


    def reset(self, state, action):
        self.state = state
        self.action = action
        self.render_character = True
        self.render_goal = True
        for tile in self.tilemap.tiles:
            if tile.texture_name == "cracked_hole":
                tile.texture_name = "hole"

    def update(self, state, action, reward, terminated):
        if terminated:
            if state == self.finish_state:
                self.render_goal = False
                settings.SOUNDS["win"].play()
            else:
                self.tilemap.tiles[state].texture_name = "cracked_hole"
                self.render_character = False
                settings.SOUNDS["ice_cracking"].play()
                settings.SOUNDS["water_splash"].play()

        self.state = state
        self.action = action

    def render(self):
        self.render_surface.fill((0, 0, 0))

        self.tilemap.render(self.render_surface)

        self.render_surface.blit(
            settings.TEXTURES["stool"],
            (self.tilemap.tiles[0].x, self.tilemap.tiles[0].y),
        )

        if self.render_goal:
            self.render_surface.blit(
                settings.TEXTURES["goal"],
                (
                    self.tilemap.tiles[self.finish_state].x,
                    self.tilemap.tiles[self.finish_state].y,
                ),
            )

        if self.render_character:
            self.render_surface.blit(
                settings.TEXTURES["character"][self.action],
                (self.tilemap.tiles[self.state].x, self.tilemap.tiles[self.state].y),
            )

        self.screen.blit(
            pygame.transform.scale(self.render_surface, self.screen.get_size()), (0, 0)
        )

        pygame.event.pump()
        pygame.display.update()

    def close(self):
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        pygame.display.quit()
        pygame.quit()
