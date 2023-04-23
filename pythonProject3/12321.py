import pygame
from pygame_gui import UIManager
from pygame_gui.elements.ui_drop_down_menu import UIDropDownMenu

# Инициализация pygame
pygame.init()

# Настройки окна
screen_width = 900
screen_height = 600
window_surface = pygame.display.set_mode((screen_width, screen_height))

# Создаем экземпляр класса UIManager
ui_manager = UIManager((screen_width, screen_height))

# Список доступных уровней
levels = ["Level 1", "Level 2", "Level 3"]

# Создаем выпадающий список с помощью класса UIDropDownMenu и устанавливаем его положение на экране
level_menu = UIDropDownMenu(levels, levels[0], pygame.Rect(0, 0, 100, 50), manager=ui_manager)

# Главный цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обновляем UIManager с помощью метода process_events
        ui_manager.process_events(event)

    # Обновляем UIManager и отрисовываем все элементы интерфейса на экране
    ui_manager.update(pygame.time.Clock().tick(60) / 1000.0)
    window_surface.fill((255, 255, 255))
    ui_manager.draw_ui(window_surface)
    pygame.display.flip()

# Выходим из pygame
pygame.quit()