import pygame
import sys

import pygame
from pygame_gui import UIManager
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu


BLOCK_SIZE = 50
WHITE = 255, 255, 255
BLACK = 0, 0, 0
BLUE = 0, 0, 255
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()


class Block:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def move(self, x, y):
        self.x = x
        self.y = y

    def update(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))


class Level:
    def __init__(self, file_name):
        self.width = 0
        self.height = 0
        self.blocks = []
        self.main_block = None
        self.main_block_index = None
        self.color_dict = {
            0: (255, 255, 255),  # white
            1: (0, 0, 0),  # black
            2: (255, 0, 0),  # red
            3: (0, 255, 0),  # green
            4: (0, 0, 255),  # blue
        }
        with open(file_name, 'r') as f:
            lines = f.readlines()
            self.height = len(lines)
            for i, line in enumerate(lines):
                row = []
                blocks_in_row = line.strip().split()
                self.width = max(self.width, len(blocks_in_row))
                for j, val in enumerate(blocks_in_row):
                    if val == '1':
                        block = Block(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, (0, 0, 0))
                        self.main_block = block
                        self.main_block_index = j

                    elif val != '0':
                        color = self.color_dict.get(int(val), (255, 255, 255))
                        row.append(Block(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE, color))
                if row:
                    self.blocks.append(row)

    def draw(self, surface):
        for row in self.blocks:
            for block in row:
                pygame.draw.rect(surface, block.color, (block.x, block.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.main_block.color, (self.main_block.x, self.main_block.y, BLOCK_SIZE, BLOCK_SIZE))

    def get_main_block(self):
        return self.main_block

    def get_color_by_index(self, index):
        return self.color_dict.get(index, (255, 255, 255))


def check_win(blocks):
    color_dict = {}
    for block in blocks:
        if block.color not in color_dict:
            color_dict[block.color] = [(block.x, block.y)]
        else:
            color_dict[block.color].append((block.x, block.y))

    for coord_list in color_dict.values():
        if len(coord_list) > 1:
            for i in range(len(coord_list) - 1):
                if abs(coord_list[i][0] - coord_list[i + 1][0]) + abs(coord_list[i][1] - coord_list[i + 1][1]) != 50:
                    return False
    return True


def game_over(message, screen, screen_width, screen_height):
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Отрисовка на экране текста
        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.update()


def draw_restart_button(screen, screen_width, screen_height):
    font = pygame.font.SysFont(None, 50)
    text = font.render("⟳", True, BLUE)
    text_rect = text.get_rect(topright=(screen_width - 10, 10))

    pygame.draw.circle(screen, BLUE, text_rect.center, text_rect.width // 2 + 5, 5)
    pygame.draw.line(screen, BLUE, (text_rect.centerx, text_rect.top + 10), (text_rect.centerx, text_rect.bottom - 10),
                     5)
    pygame.draw.line(screen, BLUE, (text_rect.left + 10, text_rect.centery), (text_rect.right - 10, text_rect.centery),
                     5)


class Game:
    def __init__(self):
        self.__screen_width = 800
        self.__screen_height = 700
        self.__block_size = 50
        self.__screen = pygame.display.set_mode((self.__screen_width, self.__screen_height))
        self._level_file_1 = 'level_1.txt'
        self.__clock = pygame.time.Clock()

        self.ui_manager = UIManager((self.__screen_width, self.__screen_height))
        self.level_list = ['Level 1', 'Level 2', 'Level 3']
        self.level_menu = UIDropDownMenu(self.level_list, self.level_list[0], pygame.Rect(0, 0, 100, 50), manager=self.ui_manager)

    def start(self):
        level_1 = Level(self._level_file_1)
        main_block = level_1.get_main_block()

        while True:
            restart_button_rect = pygame.Rect(770, 10, 60, 60)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        level_1 = Level(self._level_file_1)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        main_block = level_1.get_main_block()
                        main_block.x -= self.__block_size
                        if main_block.x < 0:
                            main_block.x = 0
                        for row in level_1.blocks:
                            for block in row:
                                if main_block != block and main_block.x == block.x and main_block.y == block.y:
                                    block.x -= self.__block_size
                                    if block.x < 0:
                                        block.x = 0
                    elif event.key == pygame.K_RIGHT:
                        main_block = level_1.get_main_block()
                        main_block.x += self.__block_size
                        if main_block.x + self.__block_size > self.__screen_width:
                            main_block.x = self.__screen_width - self.__block_size
                        for row in level_1.blocks:
                            for block in row:
                                if main_block != block and main_block.x == block.x and main_block.y == block.y:
                                    block.x += self.__block_size
                                    if block.x + self.__block_size > self.__screen_width:
                                        block.x = self.__screen_width - BLOCK_SIZE
                    elif event.key == pygame.K_UP:
                        main_block = level_1.get_main_block()
                        main_block.y -= self.__block_size
                        if main_block.y < 0:
                            main_block.y = 0
                        for row in level_1.blocks:
                            for block in row:
                                if main_block != block and main_block.x == block.x and main_block.y == block.y:
                                    block.y -= self.__block_size
                                    if block.y < 0:
                                        block.y = 0
                    elif event.key == pygame.K_DOWN:
                        main_block = level_1.get_main_block()
                        main_block.y += self.__block_size
                        if main_block.y + self.__block_size > self.__screen_height:
                            main_block.y = self.__screen_height - self.__block_size
                        for row in level_1.blocks:
                            for block in row:
                                if main_block != block and main_block.x == block.x and main_block.y == block.y:
                                    block.y += self.__block_size
                                    if block.y + self.__block_size > self.__screen_height:
                                        block.y = self.__screen_height - self.__block_size
                self.ui_manager.process_events(event)

            for i, row in enumerate(level_1.blocks):
                for j, block in enumerate(row):
                    if j == level_1.main_block_index:
                        continue
                    if block.x < level_1.get_main_block().x + BLOCK_SIZE and \
                            block.x + BLOCK_SIZE > level_1.get_main_block().x and \
                            block.y < level_1.get_main_block().y + BLOCK_SIZE and \
                            block.y + BLOCK_SIZE > level_1.get_main_block().y:
                        if level_1.get_main_block().x > block.x:
                            level_1.get_main_block().x = block.x - BLOCK_SIZE
                        elif level_1.get_main_block().x < block.x:
                            level_1.get_main_block().x = block.x + BLOCK_SIZE
                        elif level_1.get_main_block().y > block.y:
                            level_1.get_main_block().y = block.y - BLOCK_SIZE
                        else:
                            level_1.get_main_block().y = block.y + BLOCK_SIZE
            for row in level_1.blocks:
                for block in row:
                    if block != level_1.get_main_block():
                        if block.x == level_1.main_block.x and block.y == level_1.main_block.y:
                            # Move the main block back to its previous position
                            if event.key == pygame.K_LEFT:
                                level_1.main_block.x += BLOCK_SIZE
                            elif event.key == pygame.K_RIGHT:
                                level_1.main_block.x -= BLOCK_SIZE
                            elif event.key == pygame.K_UP:
                                level_1.main_block.y += BLOCK_SIZE
                            elif event.key == pygame.K_DOWN:
                                level_1.main_block.y -= BLOCK_SIZE
                            break
            # Update game state
            main_block = level_1.get_main_block()
            main_block.update(self.__screen)
            self.ui_manager.update(pygame.time.Clock().tick(60) / 1000.0)

            all_blocks = [block for row in level_1.blocks for block in row]
            blocks = [b for b in all_blocks if b is not main_block]
            if check_win(blocks):
                game_over("YOU WIN!", self.__screen, self.__screen_width, self.__screen_height)

            self.__screen.fill((255, 255, 255))

            self.ui_manager.draw_ui(self.__screen)
            level_1.draw(self.__screen)

            draw_restart_button(self.__screen, self.__screen_width, self.__screen_height)
            # Draw game world

            # Update display
            pygame.display.flip()

            # Limit framerate
            self.__clock.tick(60)


game = Game()
game.start()
pygame.quit()
