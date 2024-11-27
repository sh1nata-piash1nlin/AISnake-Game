import pygame
from Logic.ailogic import *
from Logic.ailogic import AIPlayerGameLogic


class Menu:
    def __init__(self, ui):
        self.ui = ui
        #self.selected_mode = None
        self.selected_game_mode = None
        self.map_type = None
        self.current_screen = None

        # Options for each screen
        option_names = []
        option_functions = []

        # Font handle
        self.text_font_path = r'assets/PressStart2P-Regular.ttf'
        self.title_font_path = r'assets/PressStart2P-Regular.ttf'

        # self.title_font_size = 40
        self.subtitle_font_size = 25
        self.text_font_size = 15

    # create background UI
    def background_screen(self):
        self.ui.clear_screen()

        # border create
        self.ui.display_image(3, 0, 0.15, r"assets/images/border_top_left.png")
        self.ui.display_image(self.ui.width - 67, 0, 0.15, r"assets/images/border_top_right.png")
        self.ui.display_image(self.ui.width - 67, self.ui.height - 89, 0.15, r"assets/images/border_bot_right.png")
        self.ui.display_image(3, self.ui.height - 89, 0.15, r"assets/images/border_bot_left.png")

        self.ui.display_text_center("@ HCMUTE - 2024", self.ui.height - 14, self.ui.light_red, 15, self.title_font_path)

    # function game quit
    def exit_game(self):
        pygame.quit()
        exit()

    def run_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        next_screen = self.start_screen_handle
        while True:
            next_screen = next_screen()
            if not next_screen:
                next_screen = self.start_screen_handle

    # ==========================
    #       Start screen
    # ==========================

    def start_screen_handle(self):
        self.background_screen()
        self.current_screen = 'start_screen'

        # Display start_screen unchanged things
        self.ui.display_image(self.ui.width // (10 / 4.5), self.ui.height // 3.5, 0.6,
                              r"assets/images/main_thumb.png")  # Snake thumbnail display
        self.ui.display_text_center("SNAKE GAME", self.ui.height // 4, self.ui.green, 100,
                                    self.title_font_path)  # Title display

        # options
        self.option_names = ['Play', 'Setting', 'Credit', 'Quit']
        self.option_functions = [self.start_game, self.show_setting, self.credit_screen_handle, self.exit_game]

        # Menu and event handler
        options = self.update_start_screen()
        return self.handle_events(self.update_start_screen, options)

    def update_start_screen(self, selected_option=0):
        # Options storage
        options = []
        option_left_padding = self.ui.width // 4 + 30
        first_opt_top_padding = self.ui.height // (10 / 4)

        # Options display
        for i in range(len(self.option_names)):
            color = self.ui.red if i == selected_option else self.ui.white
            options.append({
                'option_rect': self.ui.display_text(self.option_names[i], option_left_padding,
                                                    first_opt_top_padding + 40 * i, color, self.text_font_size,
                                                    self.text_font_path),
                'option_func': self.option_functions[i]
            })

        pygame.display.update()
        return options

    # ==========================
    #       Credit screen
    # ==========================

    def credit_screen_handle(self):
        self.background_screen()
        self.current_screen = 'start_screen'

        # Display title
        self.ui.display_text_center("OUR MEMBER", self.ui.height // 10, self.ui.white, self.subtitle_font_size,
                                    self.text_font_path)  # Title display

        # Options for credits
        self.option_names = [
            '22110013 Nguyen Le Tung Chi',
            '22110034 Nguyen Gia Huy',
            '221100 Do Duc Anh',
            '22110082 Nguyen Duc Tri',
            'Return'
        ]
        self.option_functions = [None, None, None, None, self.go_back]

        # Menu and event handler
        options = self.update_credit_screen()
        return self.handle_events(self.update_credit_screen, options)

    def update_credit_screen(self, selected_option=0):
        # Options storage
        options = []
        option_left_padding = self.ui.width // 6
        first_opt_top_padding = self.ui.height // 3
        line_spacing = 40  # Adjust line height for consistent spacing

        image_paths = [
            r'assets/images/mem_tchi.jpeg',
            r'assets/images/mem_jerry.jpeg',
            r'assets/images/mem_danh.jpeg',
            r'assets/images/mem_sh1nata.jpeg',
            r'assets/images/empty_border.png'  # Image for the "Return" option
        ]

        # Options display
        for i in range(len(self.option_names)):
            color = self.ui.light_blue if i == selected_option else self.ui.white
            options.append({
                'option_rect': self.ui.display_text(
                    self.option_names[i],
                    option_left_padding,
                    first_opt_top_padding + line_spacing * i,  # Use consistent spacing
                    color,
                    self.text_font_size,
                    self.text_font_path
                ),
                'option_func': self.option_functions[i]
            })

        # Member images
        img_x = self.ui.width // (5 / 3)
        img_y = self.ui.height // 3.5

        # Clear the image area before drawing
        self.ui.screen.fill((0, 0, 0), (img_x, img_y, 300, 320))

        # Load and display the selected image
        try:
            img = pygame.image.load(image_paths[selected_option])
            scaled_img = pygame.transform.scale(img, (300, 320))  # Rescale to 300x320 pixels
            self.ui.screen.blit(scaled_img, (img_x, img_y))
        except pygame.error as e:
            print(f"Error loading image: {e}")

        pygame.display.update()
        return options

    # Handle coming up events of specific screen
    def handle_events(self, update_screen, options, selected_option=0):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_RETURN and options[selected_option]['option_func']:
                        # if enter key is stroked ---> return called screen (its function) if there is
                        return options[selected_option]['option_func']

            update_screen(selected_option)

    def go_back(self):
        return self.start_screen_handle

    def show_setting(self):
        selected_option = 0
        self.option_names = ["Map with No Obstacles", "Map with Obstacles (Custom)", "Apply", "Return"]
        self.option_functions = [
            self.select_no_obstacle_map,  # Sets the map type to "no_obstacle"
            self.map_editor_screen,  # Opens the map editor
            self.apply_setting,  # Apply the selected settings
            self.go_back,  # Return to the main menu
        ]

        while True:
            self.ui.clear_screen()
            self.background_screen()

            # Display the title
            self.ui.display_text_center("SETTINGS", self.ui.height // 8, self.ui.green, 40, self.title_font_path)

            # Display the options dynamically
            options = self.update_setting_screen(selected_option)

            # Handle user input for navigation and selection
            action = self.handle_events(self.update_setting_screen, options, selected_option)
            if action:
                result = action()
                if result == "apply":
                    break

    def update_setting_screen(self, selected_option=0):
        options = []

        # Center the map selection options vertically
        map_option_start_y = self.ui.height // 2 - 50  # Centered vertically with some padding

        # Display map selection options
        for i in range(2):  # First two options (Map with No Obstacles, Map with Obstacles)
            color = self.ui.light_blue if i == selected_option else self.ui.white
            options.append({
                "option_rect": self.ui.display_text(self.option_names[i],
                                                    self.ui.width // 2 - 150,  # Centered horizontally
                                                    map_option_start_y + i * 50,  # Vertical spacing
                                                    color, self.text_font_size,
                                                    self.text_font_path),
                "option_func": self.option_functions[i]
            })

        # Display "Apply" button (Bottom-middle of the screen)
        apply_color = self.ui.light_blue if selected_option == 2 else self.ui.white
        options.append({
            "option_rect": self.ui.display_text(self.option_names[2],
                                                self.ui.width // 2 - 50,  # Centered horizontally
                                                self.ui.height - 250,  # Slightly above the bottom
                                                apply_color, self.text_font_size,
                                                self.text_font_path),
            "option_func": self.option_functions[2]
        })

        # Display "Return" button (Bottom-middle of the screen, below "Apply")
        return_color = self.ui.light_blue if selected_option == 3 else self.ui.white
        options.append({
            "option_rect": self.ui.display_text(self.option_names[3],
                                                self.ui.width // 2 - 50,  # Centered horizontally
                                                self.ui.height - 200,  # Below "Apply"
                                                return_color, self.text_font_size,
                                                self.text_font_path),
            "option_func": self.option_functions[3]
        })

        pygame.display.update()
        return options

    def select_no_obstacle_map(self):
        self.map_type = "no_obstacle"

    def select_obstacle_map(self):
        self.map_type = "obstacle"

    def apply_setting(self):
        print(f"Settings applied: Map type is {self.map_type}")
        return "apply"

    def show_map_selection(self):
        while True:
            self.ui.clear_screen()
            title = self.title_font.render("Choose map", True, (255, 255, 255))
            no_obstacle_button = self.button_font.render("Map with no obstacles", True, (255, 255, 255))
            obstacle_button = self.button_font.render("Map with obstacles", True, (255, 255, 255))
            back_button = self.button_font.render("Return", True, (255, 255, 255))

            spacing = 20
            self.no_obstacle_rect = self.ui.screen.blit(no_obstacle_button, [self.ui.width / 4, self.ui.height / 2])
            self.obstacle_rect = self.ui.screen.blit(obstacle_button, [self.ui.width / 4,
                                                                       self.ui.height / 2 + no_obstacle_button.get_height() + spacing])
            self.back_button_rect = self.ui.screen.blit(back_button, [10, 10])

            self.ui.screen.blit(title, [self.ui.width / 4, self.ui.height / 4])

            pygame.display.update()

    def handle_map_selection_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.no_obstacle_rect.collidepoint(event.pos):
                        self.map_type = "no_obstacle"
                        self.start_game()
                    elif self.obstacle_rect.collidepoint(event.pos):
                        self.map_type = "obstacle"
                        self.start_game()
                    elif self.back_button_rect.collidepoint(event.pos):
                        self.go_back()

    def map_editor_screen(self):
        clock = pygame.time.Clock()
        grid_color = self.ui.gray
        obstacles = set()  # To store obstacle positions

        # Load the obstacle image
        obstacle_image = pygame.image.load("assets/greenpile.jpg")
        obstacle_image = pygame.transform.scale(obstacle_image, (self.ui.snake_block, self.ui.snake_block))

        # Button states
        selected_button = 0  # 0 for "Obstacles", 1 for "Apply"
        obstacle_active = False  # True when "Obstacles" is activated with Enter

        # Button positions
        button_width, button_height = 200, 50
        obstacle_button_rect = pygame.Rect(self.ui.width - 300, 200, button_width, button_height)
        apply_button_rect = pygame.Rect(self.ui.width - 300, 270, button_width, button_height)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse button clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos

                    # Check if "Obstacles" button is clicked
                    if obstacle_button_rect.collidepoint(mouse_x, mouse_y):
                        selected_button = 0  # Highlight "Obstacles" button
                        obstacle_active = True

                    # Check if "Apply" button is clicked
                    elif apply_button_rect.collidepoint(mouse_x, mouse_y):
                        # Save the map and return to the start menu
                        self.map_type = "custom_obstacle"
                        self.custom_map = {"obstacles": obstacles}
                        return  # Exit the editor and save the map

                # Navigate buttons with UP/DOWN keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_button = (selected_button - 1) % 2  # Wrap around between buttons
                    elif event.key == pygame.K_DOWN:
                        selected_button = (selected_button + 1) % 2  # Wrap around between buttons
                    elif event.key == pygame.K_RETURN:
                        # Select the active button
                        if selected_button == 0:  # "Obstacles" selected
                            obstacle_active = True  # Activate obstacle placement
                        elif selected_button == 1:  # "Apply" selected
                            self.map_type = "custom_obstacle"
                            self.custom_map = {"obstacles": obstacles}
                            return  # Exit the editor and save the map

            # Continuously place obstacles if "Obstacles" button is active and "O" is held
            keys = pygame.key.get_pressed()
            if keys[pygame.K_o] and obstacle_active:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = (mouse_x - self.ui.grid_pos) // self.ui.snake_block
                grid_y = (mouse_y - self.ui.grid_pos) // self.ui.snake_block
                if 0 <= grid_x < self.ui.cols and 0 <= grid_y < self.ui.rows:
                    obstacles.add((grid_y, grid_x))  # Add to obstacles set

            # Draw the grid
            self.ui.clear_screen()
            self.ui.draw_grid()

            # Draw obstacles using the obstacle image
            for obstacle in obstacles:
                self.ui.screen.blit(
                    obstacle_image,
                    (
                        self.ui.grid_pos + obstacle[1] * self.ui.snake_block,
                        self.ui.grid_pos + obstacle[0] * self.ui.snake_block,
                    ),
                )

            # Draw buttons on the right without borders
            obstacle_text_color = self.ui.blue if obstacle_active else (
                self.ui.green if selected_button == 0 else self.ui.white)
            self.ui.display_text("Obstacles", obstacle_button_rect.x + 30, obstacle_button_rect.y + 15,
                                 obstacle_text_color, 25)

            apply_text_color = self.ui.green if selected_button == 1 else self.ui.white
            self.ui.display_text("Apply", apply_button_rect.x + 60, apply_button_rect.y + 15, apply_text_color, 25)

            pygame.display.update()
            clock.tick(30)  # 30 FPS

    def start_game(self):

        if not self.map_type:
            self.show_popup_message("You must set Setting first before playing!")
            return  # Exit the function if map_type is not set

        game_logic = None

        if self.map_type == "no_obstacle":
            game_logic = AIPlayerGameLogic(self.ui, (self.ui.rows // 2, self.ui.cols // 2))
        elif self.map_type == "custom_obstacle":
            obstacles = self.custom_map["obstacles"]
            game_logic = AIPlayerGameLogic(self.ui, (self.ui.rows // 2, self.ui.cols // 2))
            game_logic.obstacles = obstacles
        else:
            print("Error: Invalid map type!")
            return

        if game_logic:
            game_logic.game_loop()

    def show_popup_message(self, message):
        font = pygame.font.Font(self.title_font_path, 20)
        text_surface = font.render(message, True, self.ui.red)

        # Position the message just above "HCMUTE 2024" at the bottom
        text_x = self.ui.width // 2
        text_y = self.ui.height - 300  # Slightly above the bottom of the screen
        text_rect = text_surface.get_rect(center=(text_x, text_y))

        clock = pygame.time.Clock()

        # Keep the popup displayed until the user presses Enter or Esc
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    # Dismiss the popup if the user presses Enter or Esc
                    if event.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                        return  # Exit the popup

            self.ui.clear_screen()
            self.background_screen()  # Draw the static background (without re-rendering the start screen)

            # Draw the popup message
            self.ui.screen.blit(text_surface, text_rect)

            # Display footer (e.g., "@ HCMUTE - 2024")
            self.ui.display_text_center("@ HCMUTE - 2024", self.ui.height - 14, self.ui.light_red, 15,
                                        self.title_font_path)

            pygame.display.update()
            clock.tick(30)  # 30 FPS
