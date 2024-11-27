import pygame
from UI.window import UI
from Logic.ailogic import *
from menu import Menu


def main():
    pygame.init()

    base_ui = UI()

    menu = Menu(base_ui)

    menu.run_menu()
    pygame.quit()

if __name__ == "__main__":
    main()
