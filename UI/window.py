import pygame

class UI:
    def __init__(self):
        self.width, self.height = 1000, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (90, 166, 110)
        self.blue = (0, 0, 255)
        self.light_blue = (2, 242, 219)
        self.light_red = (255, 182, 193)
        self.dark_green = (7, 90, 102)
        self.dark_blue = (8, 111, 158)
        self.gray = (34, 34, 34)

        self.default_font_path = r'assets/PressStart2P-Regular.ttf'

        self.background = pygame.image.load('assets/background2.jpeg')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))

        # Define cell size
        self.snake_block = 10
        # Top and left padding for grid, grid position (top left) will start here
        self.grid_pos = self.height // 20
        # Grid height is 90% window height
        self.rows = int((self.height * 0.9) // self.snake_block)
        # Grid width is 60% window width
        self.cols = int((self.width * 0.6) // self.snake_block)

    def draw_snake(self, snake_list, color):
        for position in snake_list:
            pygame.draw.rect(self.screen, color, [self.grid_pos + position[1] * self.snake_block,
                                                  self.grid_pos + position[0] * self.snake_block, self.snake_block,
                                                  self.snake_block])

    def draw_food(self, food_position, color):
        food_row, food_col = food_position
        pygame.draw.rect(self.screen, color,
                         [self.grid_pos + food_col * self.snake_block, self.grid_pos + food_row * self.snake_block,
                          self.snake_block, self.snake_block])

    def draw_obstacles(self, obstacles_position_list):
        """
        Draw obstacles on the grid using an obstacle image.
        :param obstacles_position_list: List or set of obstacle positions [(row, col), ...]
        """
        # Load the obstacle image
        obstacle_img = pygame.image.load(r'assets/greenpile.jpg')
        obstacle_img = pygame.transform.scale(obstacle_img, (self.snake_block, self.snake_block))

        # Draw each obstacle at its respective grid position
        for position in obstacles_position_list:
            self.screen.blit(
                obstacle_img,
                (
                    self.grid_pos + position[1] * self.snake_block,  # X-coordinate
                    self.grid_pos + position[0] * self.snake_block,  # Y-coordinate
                ),
            )

    def display_message(self, message):
        font_style = pygame.font.Font(self.default_font_path, 15)
        mesg = font_style.render(message, True, self.red)
        self.screen.blit(mesg, [self.width / 6, self.height / 3])

    def refresh_screen(self):
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(self.black)

    def draw_grid(self):
        grid_color = self.gray
        grid_width = self.cols * self.snake_block
        grid_height = self.rows * self.snake_block
        for row in range(self.rows + 1):
            start_point_y = self.grid_pos + row * self.snake_block
            pygame.draw.line(self.screen, grid_color, (self.grid_pos, start_point_y),
                             (self.grid_pos + grid_width, start_point_y))
        for col in range(self.cols + 1):
            start_point_x = self.grid_pos + col * self.snake_block
            pygame.draw.line(self.screen, grid_color, (start_point_x, self.grid_pos),
                             (start_point_x, self.grid_pos + grid_height))

    def display_text(self, text, x, y, color, size, font_path=None):
        font_path = self.default_font_path
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(text, True, color)
        return self.screen.blit(text_surface, (x, y))

    def display_text_center(self, text, y, color, size, font_path=None):
        font_path = self.default_font_path
        font = pygame.font.Font(font_path, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(self.width // 2, y))
        return self.screen.blit(text_surface, text_rect)

    def display_image(self, x, y, scale_rate, img_path):
        image = pygame.image.load(img_path)
        image = pygame.transform.scale(image, (image.get_width() * scale_rate, image.get_height() * scale_rate))
        return self.screen.blit(image, (x, y))
