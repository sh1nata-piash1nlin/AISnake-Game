import pygame
from UI.window import UI
from menu import Menu

def main():
    pygame.init()

    ui = UI()

    menu = Menu(ui)

    menu.run_menu()

    pygame.quit()

if __name__ == "__main__":
    main()
