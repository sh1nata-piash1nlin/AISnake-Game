import pygame


class Menu:
    def __init__(self, ui):
        self.ui = ui
        self.selected_mode = None
        self.selected_game_mode = None
        self.map_type = None
        self.start_button_rect = None
        self.no_obstacle_rect = None
        self.obstacle_rect = None
        self.back_button_rect = None
        self.exit_button_rect = None

    def run_menu(self):
        while True:
            self.ui.clear_screen()
            self.show_start_menu()
            pygame.display.update()
            self.handle_events()

    def show_start_menu(self):
        # Title
        font_title = self.ui.get_font(60)
        title = font_title.render("Snake Game", True, (242, 172, 205))
        shadow = font_title.render("Snake Game", True, (237, 138, 185))

        self.ui.screen.blit(shadow, [self.ui.width / 2 - title.get_width() / 2 + 3, self.ui.height / 4 + 3])
        self.ui.screen.blit(title, [self.ui.width / 2 - title.get_width() / 2, self.ui.height / 4])

        # Buttons start quit
        font_button = self.ui.get_font(30)
        button_width = 200
        button_height = 60
        button_spacing = 20

        start_button_x = self.ui.width / 2 - button_width / 2
        start_button_y = self.ui.height / 2
        exit_button_x = self.ui.width / 2 - button_width / 2
        exit_button_y = start_button_y + button_height + button_spacing

        mouse_pos = pygame.mouse.get_pos()
        start_color = (255, 255, 0) if pygame.Rect(start_button_x, start_button_y, button_width,
                                                   button_height).collidepoint(mouse_pos) else (255, 255, 255)
        exit_color = (255, 255, 0) if pygame.Rect(exit_button_x, exit_button_y, button_width,
                                                  button_height).collidepoint(mouse_pos) else (255, 255, 255)

        # Render Start Button
        pygame.draw.rect(self.ui.screen, (66, 192, 104), (start_button_x, start_button_y, button_width, button_height),
                         border_radius=10)
        start_button = font_button.render("Start", True, start_color)
        self.start_button_rect = self.ui.screen.blit(start_button, (
            start_button_x + (button_width - start_button.get_width()) / 2,
            start_button_y + (button_height - start_button.get_height()) / 2))

        # Render Exit Button
        pygame.draw.rect(self.ui.screen, (66, 192, 104), (exit_button_x, exit_button_y, button_width, button_height),
                         border_radius=10)
        exit_button = font_button.render("Quit", True, exit_color)
        self.exit_button_rect = self.ui.screen.blit(exit_button, (
            exit_button_x + (button_width - exit_button.get_width()) / 2,
            exit_button_y + (button_height - exit_button.get_height()) / 2))

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.start_button_rect and self.start_button_rect.collidepoint(event.pos):
                    self.show_map_selection()
                elif self.exit_button_rect and self.exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    exit()

    def show_map_selection(self):
        running = True
        while running:
            self.ui.clear_screen()

            # Title
            font_title = self.ui.get_font(30)
            title_text = "Choose map type"
            title_shadow = font_title.render(title_text, True, (237, 138, 185))
            title = font_title.render(title_text, True, (242, 172, 205))

            title_x = (self.ui.width - title.get_width()) / 2
            title_y = (self.ui.height / 4) - (title.get_height() / 2)

            self.ui.screen.blit(title_shadow, [title_x + 3, title_y + 3])
            self.ui.screen.blit(title, [title_x, title_y])

            # Buttons
            font_button = self.ui.get_font(20)
            button_width = 500
            button_height = 60
            button_spacing = 20

            no_obstacle_button_x = (self.ui.width - button_width) / 2
            no_obstacle_button_y = self.ui.height / 2
            obstacle_button_x = no_obstacle_button_x
            obstacle_button_y = no_obstacle_button_y + button_height + button_spacing

            mouse_pos = pygame.mouse.get_pos()
            no_obstacle_color = (255, 255, 0) if pygame.Rect(no_obstacle_button_x, no_obstacle_button_y, button_width,
                                                             button_height).collidepoint(mouse_pos) else (255, 255, 255)
            obstacle_color = (255, 255, 0) if pygame.Rect(obstacle_button_x, obstacle_button_y, button_width,
                                                          button_height).collidepoint(mouse_pos) else (255, 255, 255)

            # Render No Obstacle Button
            pygame.draw.rect(self.ui.screen, (66, 192, 104),
                             (no_obstacle_button_x, no_obstacle_button_y, button_width, button_height), border_radius=10)
            no_obstacle_button = font_button.render("No Obstacles", True, no_obstacle_color)
            self.no_obstacle_rect = self.ui.screen.blit(no_obstacle_button, (
                no_obstacle_button_x + (button_width - no_obstacle_button.get_width()) / 2,
                no_obstacle_button_y + (button_height - no_obstacle_button.get_height()) / 2))

            # Render Obstacles Button
            pygame.draw.rect(self.ui.screen, (66, 192, 104),
                             (obstacle_button_x, obstacle_button_y, button_width, button_height), border_radius=10)
            obstacle_button = font_button.render("With Obstacles", True, obstacle_color)
            self.obstacle_rect = self.ui.screen.blit(obstacle_button, (
                obstacle_button_x + (button_width - obstacle_button.get_width()) / 2,
                obstacle_button_y + (button_height - obstacle_button.get_height()) / 2))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.no_obstacle_rect and self.no_obstacle_rect.collidepoint(event.pos):
                        self.map_type = "no_obstacle"
                        running = False
                        self.game_design()
                    elif self.obstacle_rect and self.obstacle_rect.collidepoint(event.pos):
                        self.map_type = "obstacle"
                        running = False
                        self.game_design()

    def no_obstacle_map(self):
        running = True
        map_width, map_height = 850, 650
        grid_size = 28
        cell_size = map_width // grid_size - 6  # Size of each grid cell
        margin_x = (self.ui.width - map_width) // 2
        margin_y = (self.ui.height - map_height) // 2 - 10

        # Load flag and obstacle images
        flag_img = pygame.image.load('assets/flag.jpg')  # Ensure this file is in your assets folder
        flag_img = pygame.transform.scale(flag_img, (cell_size, cell_size))
        flag_position = None
        dragging_flag = False

        button_font = self.ui.get_font(20)
        start_button_rect = pygame.Rect(self.ui.width - 360, 350, 250, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse events
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    # Start button clicked
                    if start_button_rect.collidepoint(mouse_pos):
                        dragging_flag = True  # Enable dragging
                        if flag_position is None:  # Initialize flag's position on the map
                            flag_position = [margin_x, margin_y]

                    # Check if clicking inside the flag's position to start dragging
                    if flag_position and dragging_flag:
                        flag_rect = pygame.Rect(flag_position[0], flag_position[1], cell_size, cell_size)
                        if flag_rect.collidepoint(mouse_pos):
                            dragging_flag = True

                # Handle flag dragging
                if event.type == pygame.MOUSEMOTION and dragging_flag and flag_position:
                    # Update the flag's position as the mouse moves
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    flag_position[0] = mouse_x - cell_size // 2  # Center flag under cursor
                    flag_position[1] = mouse_y - cell_size // 2

                # Handle mouse release (drop the flag)
                if event.type == pygame.MOUSEBUTTONUP and dragging_flag:
                    dragging_flag = False
                    if flag_position:
                        # Snap flag to the nearest grid cell
                        flag_position[0] = ((flag_position[0] - margin_x) // cell_size) * cell_size + margin_x
                        flag_position[1] = ((flag_position[1] - margin_y) // cell_size) * cell_size + margin_y

                        # Limit flag to map boundaries
                        if not (margin_x <= flag_position[0] < margin_x + map_width and
                                margin_y <= flag_position[1] < margin_y + map_height):
                            flag_position = None  # Reset position if dropped outside the map

            # Clear the screen with a solid black color
            self.ui.screen.fill(self.ui.black)

            # Draw the map grid with grey cells
            for row in range(grid_size):
                for col in range(grid_size):
                    rect_x = margin_x + col * cell_size
                    rect_y = margin_y + row * cell_size
                    pygame.draw.rect(self.ui.screen, (169, 169, 169), (rect_x, rect_y, cell_size, cell_size), 0)
                    pygame.draw.rect(self.ui.screen, self.ui.white, (rect_x, rect_y, cell_size, cell_size), 1)

            # Draw the flag if it exists
            if flag_position:
                self.ui.screen.blit(flag_img, flag_position)

            # Draw the "Start" button
            pygame.draw.rect(self.ui.screen, (66, 192, 104), start_button_rect)
            start_text = button_font.render("Start", True, self.ui.white)
            self.ui.screen.blit(start_text,
                                (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                                 start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))

            pygame.display.update()

    def obstacle_map(self):
        running = True
        map_width, map_height = 850, 650
        grid_size = 28
        cell_size = map_width // grid_size - 6  # Size of each grid cell
        margin_x = (self.ui.width - map_width) // 2
        margin_y = (self.ui.height - map_height) // 2 - 10

        # Load flag and obstacle images
        flag_img = pygame.image.load('assets/flag.jpg')  # Ensure this file is in your assets folder
        flag_img = pygame.transform.scale(flag_img, (cell_size, cell_size))
        obstacle_img = pygame.image.load('assets/greenpile.jpg')
        obstacle_img = pygame.transform.scale(obstacle_img, (cell_size, cell_size))

        flag_position = None
        dragging_flag = False
        obstacles = []

        # Button properties
        button_font = self.ui.get_font(20)
        start_button_rect = pygame.Rect(self.ui.width - 360, 315, 250, 50)
        obstacle_button_rect = pygame.Rect(self.ui.width - 360, 385, 250, 50)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle mouse events
                mouse_pos = pygame.mouse.get_pos()

                # Handle button clicks
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Start button clicked
                    if start_button_rect.collidepoint(mouse_pos):
                        mode = "start"  # Switch to flag placement mode
                        dragging_flag = True
                        if flag_position is None:
                            flag_position = [margin_x, margin_y]

                    # Obstacles button clicked
                    if obstacle_button_rect.collidepoint(mouse_pos):
                        mode = "obstacle"  # Switch to obstacle placement mode

                # Handle flag dragging in "start" mode
                if event.type == pygame.MOUSEMOTION and dragging_flag and mode == "start":
                    flag_position[0] = mouse_pos[0] - cell_size // 2  # Center flag under cursor
                    flag_position[1] = mouse_pos[1] - cell_size // 2

                # Handle flag drop in "start" mode
                if event.type == pygame.MOUSEBUTTONUP and dragging_flag and mode == "start":
                    dragging_flag = False
                    if flag_position:
                        # Snap flag to the nearest grid cell
                        flag_position[0] = ((flag_position[0] - margin_x) // cell_size) * cell_size + margin_x
                        flag_position[1] = ((flag_position[1] - margin_y) // cell_size) * cell_size + margin_y

                        # Limit flag to map boundaries
                        if not (margin_x <= flag_position[0] < margin_x + map_width and
                                margin_y <= flag_position[1] < margin_y + map_height):
                            flag_position = None  # Reset position if dropped outside the map

                # Handle obstacle placement in "obstacle" mode
                if event.type == pygame.KEYDOWN and event.key == pygame.K_o and mode == "obstacle":
                    # Place an obstacle at the mouse position
                    if margin_x <= mouse_pos[0] < margin_x + map_width and margin_y <= mouse_pos[
                        1] < margin_y + map_height:
                        grid_x = (mouse_pos[0] - margin_x) // cell_size
                        grid_y = (mouse_pos[1] - margin_y) // cell_size
                        if (grid_x, grid_y) not in obstacles:  # Avoid duplicate obstacles
                            obstacles.append((grid_x, grid_y))

            # Clear the screen with a solid black color
            self.ui.screen.fill(self.ui.black)

            # Draw the map grid with grey cells
            for row in range(grid_size):
                for col in range(grid_size):
                    rect_x = margin_x + col * cell_size
                    rect_y = margin_y + row * cell_size
                    pygame.draw.rect(self.ui.screen, (169, 169, 169), (rect_x, rect_y, cell_size, cell_size), 0)
                    pygame.draw.rect(self.ui.screen, self.ui.white, (rect_x, rect_y, cell_size, cell_size), 1)

            # Draw obstacles
            for obstacle in obstacles:
                obs_x = margin_x + obstacle[0] * cell_size
                obs_y = margin_y + obstacle[1] * cell_size
                self.ui.screen.blit(obstacle_img, (obs_x, obs_y))

            # Draw the flag if it exists
            if flag_position:
                self.ui.screen.blit(flag_img, flag_position)

            # Draw the "Start" and "Obstacles" buttons
            pygame.draw.rect(self.ui.screen, (66, 192, 104), start_button_rect)
            start_text = button_font.render("Start", True, self.ui.white)
            self.ui.screen.blit(start_text,
                                (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                                 start_button_rect.y + (
                                         start_button_rect.height - start_text.get_height()) // 2))

            pygame.draw.rect(self.ui.screen, (66, 192, 104), obstacle_button_rect)
            obstacle_text = button_font.render("Obstacles", True, self.ui.white)
            self.ui.screen.blit(obstacle_text, (
                obstacle_button_rect.x + (obstacle_button_rect.width - obstacle_text.get_width()) // 2,
                obstacle_button_rect.y + (obstacle_button_rect.height - obstacle_text.get_height()) // 2))

            pygame.display.update()

    # game design
    def game_design(self):
        if self.map_type == "no_obstacle":
            self.no_obstacle_map()
        if self.map_type == "obstacle":
            self.obstacle_map()

    #tao them 1 button next nua o moi map
    #bam next thi se chuyen sang game ( co snake, co xuat hien Food ) 
    # giao dien thi co cac thuat toan DFS, BFS, A* v.v 
    # set timer cho cac thuat toan ......

# Run the menu

