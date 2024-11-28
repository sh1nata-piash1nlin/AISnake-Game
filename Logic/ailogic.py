import pygame
import random
from collections import deque
import heapq
from FinalProject.UI.SliderSpeed import Slider

class Pathfinding:
    def __init__(self, map_size):
        self.numb_rows, self.numb_cols = map_size
        self.path_algorithm = {
            'bfs': self.bfs,
            'dfs': self.dfs,
            'astar': self.a_star,
            'hill': self.hill_climbing,
            'beam': self.beam_search,
            'current': self.bfs  # Default algorithm
        }
        self.directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_neighbors(self, position):
        """
        Return the neighbors of a given position that does not accross boudaries.
        """
        row, col = position
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.numb_rows) and (0 <= new_col < self.numb_cols):
                neighbors.append((new_row, new_col))

        return neighbors

    def bfs(self, start, goal, obstacles_list):
        queue = deque([start])
        came_from = {start: None}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            current = queue.popleft()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                # Neighbor accrosses boudary
                if (neighbor[0] < 0) or (neighbor[0] >= self.numb_rows) or (neighbor[1] < 0) or (
                        neighbor[1] >= self.numb_cols):
                    continue

                # Neighbor is visited or neighbor is obstacles_list (grid obstacles and snake included)
                if neighbor in came_from or neighbor in obstacles_list:
                    continue

                # True case
                queue.append(neighbor)
                came_from[neighbor] = current

        return []

    def dfs(self, start, goal, obstacles_list):
        stack = [start]
        came_from = {start: None}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while stack:
            current = stack.pop()
            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (neighbor[0] < 0) or (neighbor[0] >= self.numb_rows) or (neighbor[1] < 0) or (
                        neighbor[1] >= self.numb_cols):
                    continue

                if neighbor in came_from or neighbor in obstacles_list:
                    continue

                stack.append(neighbor)
                came_from[neighbor] = current

        return []

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start, goal, obstacles_list):
        open_set = []  # Priority queue
        heapq.heappush(open_set, (0, start))
        came_from = {start: None}
        g_score = {start: 0}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while open_set:
            # Get the node with the lowest f_score / (score, node)
            current_priority, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct the path
                path = []
                while current:
                    path.append(current)
                    current = came_from[current]
                return path[::-1][1:]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                # Check if the neighbor is out of bounds
                if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                        neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                    continue

                # Check if the neighbor is an obstacle or already visited
                if neighbor in obstacles_list or neighbor in came_from:
                    continue

                # Actual cost from start to neighbor, use to check if the path is shorter
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, neighbor))
                    came_from[neighbor] = current

        return []

    def hill_climbing(self, start, goal, obstacles_list):
        current = start
        came_from = {start: None}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while current != goal:
            neighbors = []

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                        neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                    continue

                if neighbor in obstacles_list or neighbor in came_from:
                    continue

                neighbors.append((self.heuristic(neighbor, goal), neighbor))

            # If no valid neighbors, we are stuck. Backtrack to the previous node can solve this but I think it's not necessary due to our purpose of making this game.
            if not neighbors:
                return []

            # Select the neighbor with the best heuristic value (greedy choice)
            next_step = min(neighbors, key=lambda x: x[0])[1]

            came_from[next_step] = current
            current = next_step

        path = []
        while current:
            path.append(current)
            current = came_from[current]

        return path[::-1][1:]

    def beam_search(self, start, goal, obstacles_list, beam_width=2):
        open_set = [(self.heuristic(start, goal), start)]
        came_from = {start: None}
        g_score = {start: 0}
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while open_set:
            # Use new_open_set to store the best nodes
            new_open_set = []

            for _, current in open_set:
                if current == goal:
                    path = []
                    while current:
                        path.append(current)
                        current = came_from[current]
                    return path[::-1][1:]

                for direction in directions:
                    neighbor = (current[0] + direction[0], current[1] + direction[1])

                    if (neighbor[0] < 0 or neighbor[0] >= self.numb_rows or
                            neighbor[1] < 0 or neighbor[1] >= self.numb_cols):
                        continue

                    if neighbor in obstacles_list or neighbor in came_from:
                        continue

                    tentative_g_score = g_score[current] + 1
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)

                    new_open_set.append((f_score, neighbor))
                    came_from[neighbor] = current

                    g_score[neighbor] = tentative_g_score

            # Choose the best nodes from new_open_set
            open_set = sorted(new_open_set, key=lambda x: x[0])[:beam_width]

        return []

    def flood_fill(self, position, obstacles_list):
        """
        This function is used to count the number of reachable cells from a given position.
        """
        visited = set()
        stack = [position]
        count = 0

        while stack:
            current = stack.pop()
            if current in visited or current in obstacles_list:
                continue
            visited.add(current)
            count += 1
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited and neighbor not in obstacles_list:
                    stack.append(neighbor)

        return count

    def find_safe_move(self, obstacles, head_pos):
        """
        Find the best move that has the most empty cells around it.
        """
        neighbors = self.get_neighbors(head_pos)
        max_space = 0
        best_move = None

        for neighbor in neighbors:
            if neighbor not in obstacles:
                # Count the number of reachable cells from this neighbor
                space = self.flood_fill(neighbor, obstacles)
                if space > max_space:
                    max_space = space
                    best_move = neighbor

        return best_move

    def find_path(self, start, goal, obstacles, algorithm):
        return algorithm(start, goal, obstacles)

class BaseGameLogic:
    def __init__(self, obstacles, map_size, initial_pos):
        self.obstacles = obstacles  # Initialize obstacles
        self.numb_rows, self.numb_cols = map_size
        self.initial_pos_row, self.initial_pos_col = initial_pos

        self.snake_speed = 50 # Default velocity
        self.target_score = 150 #  Target score to stop the game
        self.clock = pygame.time.Clock()
        self.start_time = None # Initialize the timer

        self.reset_game()

    def reset_game(self):
        # Set start position
        self.head_row = self.initial_pos_row
        self.head_col = self.initial_pos_col

        self.snake_list = [(self.head_row, self.head_col)]
        self.length_of_snake = 1
        self.score = 0
        self.game_close = False

        self.food_row, self.food_col = self.generate_random_food_position()
        self.move_direction = [1, 0]

    def generate_random_food_position(self):
        # Create valid position list for food
        valid_positions = [
            (row_pos, col_pos)
            for row_pos in range(self.numb_rows)
            for col_pos in range(self.numb_cols)
            if (row_pos, col_pos) not in self.obstacles and (row_pos, col_pos) not in self.snake_list
        ]
        # No valid position
        if not valid_positions:
            return None

        # Return a value in valid list
        return random.choice(valid_positions)

    def update_snake_position(self):
        self.head_row += self.move_direction[0]
        self.head_col += self.move_direction[1]

        # Update new head position
        self.snake_list.append((self.head_row, self.head_col))
        # Check for length (in case no food is eaten or food is just eaten)
        if len(self.snake_list) > self.length_of_snake:
            # Del first element = tail of snake when no food is eaten, snake is moving only
            del self.snake_list[0]

    def check_boundaries(self):
        if (self.head_row < 0) or (self.head_row >= self.numb_rows) or (self.head_col < 0) or (
                self.head_col >= self.numb_cols):
            self.game_over = True

    def check_collisions(self):
        # Check if the snake's head collides with its body
        if (self.head_row, self.head_col) in self.snake_list[:-1]:
            self.game_over = True

        # Check if the snake's head collides with any obstacles
        if (self.head_row, self.head_col) in self.obstacles:
            self.game_over = True

    def check_eat_food(self):
        if self.head_row == self.food_row and self.head_col == self.food_col:
            # Update new food position and some states
            self.food_row, self.food_col = self.generate_random_food_position()
            self.length_of_snake += 1
            self.score += 1

    def handle_game_close_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.game_over = False
                    self.game_close = True
                if event.key == pygame.K_c:
                    self.reset_game()

class AIPlayerGameLogic(BaseGameLogic):
    def __init__(self, ui, initial_pos):
        super().__init__(set(), (ui.rows, ui.cols), initial_pos)
        self.pathfinding = Pathfinding((self.numb_rows, self.numb_cols))
        self.game_close = False
        self.ui = ui
        self.path = []

    def find_move(self):
        if not self.path:
            snake_as_obstacles = set(tuple(block) for block in self.snake_list)
            # Union obstacles and snake position
            obstacles_and_snake = self.obstacles | snake_as_obstacles
            start = (self.head_row, self.head_col)
            goal = (self.food_row, self.food_col)
            self.path = self.pathfinding.find_path(start, goal, obstacles_and_snake,
                                                   self.pathfinding.path_algorithm['bfs'])

            if not self.path:  # if it still can't find a path
                safe_move = self.pathfinding.find_safe_move(obstacles_and_snake, (self.head_row, self.head_col))
                if safe_move:
                    self.path = [safe_move]
                else:
                    # If there is no safe move, the snake will move randomly and probably die
                    self.path = []

        if self.path:
            next_move = self.path.pop(0)
            self.move_direction[0] = next_move[0] - self.head_row
            self.move_direction[1] = next_move[1] - self.head_col


    # ==========================
    #       GAME PLAYING screen
    # ==========================

    # GAME PLAYING SCREEN
    def game_loop(self):
        # Initialize variables for start button and algorithm dropdown
        start_button_rect = pygame.Rect(self.ui.width - 265, 420, 150, 50)
        algorithm_button_rect = pygame.Rect(self.ui.width - 280, 220, 210, 50)
        dropdown_active = False
        dropdown_options = ["BFS", "DFS", "A*", "Hill Climbing", "Beam Search"]
        algorithm_mapping = {
            "BFS": "bfs",
            "DFS": "dfs",
            "A*": "astar",
            "Hill Climbing": "hill",
            "Beam Search": "beam"
        }
        selected_algorithm_index = 0  # Default to BFS
        game_started = False  # Flag to control when the game starts
        target_reached = False  # To check if the target is reached
        end_message_displayed = False  # Whether to display Target Reached/Unreached message

        slider = Slider(self.ui.width - 250, 100, 150, 50, 60, self.snake_speed)
        self.game_over = False

        timer_start = None  # To store when the game starts

        while not self.game_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_close = True

                    # Handle UP, DOWN, and ENTER keys for dropdown
                    if dropdown_active:
                        if event.key == pygame.K_DOWN:
                            selected_algorithm_index = (selected_algorithm_index + 1) % len(dropdown_options)
                        elif event.key == pygame.K_UP:
                            selected_algorithm_index = (selected_algorithm_index - 1) % len(dropdown_options)
                        elif event.key == pygame.K_RETURN:
                            dropdown_active = False  # Close dropdown

                    # Handle ENTER to toggle dropdown when not active
                    elif event.key == pygame.K_RETURN and algorithm_button_rect.collidepoint(pygame.mouse.get_pos()):
                        dropdown_active = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    # Start button click detection
                    if start_button_rect.collidepoint(mouse_pos):
                        game_started = True  # Enable the snake to move
                        timer_start = pygame.time.get_ticks()  # Start the timer

                    # Algorithm button click detection (toggle dropdown)
                    elif algorithm_button_rect.collidepoint(mouse_pos):
                        dropdown_active = not dropdown_active

                # Slider update
                slider.update(event)

            # Game starts only if the Start button is clicked
            if game_started and not target_reached:
                self.snake_speed = int(slider.value)  # Update speed dynamically

                # Update algorithm selection
                selected_algorithm = dropdown_options[selected_algorithm_index]
                selected_algorithm_key = algorithm_mapping[selected_algorithm]  # Use the mapping dictionary
                self.pathfinding.path_algorithm['current'] = self.pathfinding.path_algorithm[selected_algorithm_key]

                self.find_move()
                self.update_snake_position()
                self.check_collisions()
                self.check_boundaries()
                self.check_eat_food()

                # Check if the target score is reached
                if self.score >= self.target_score:
                    target_reached = True
                    game_started = False  # Stop the game
                    elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000

            # Drawing UI elements
            self.ui.clear_screen()
            self.ui.draw_grid()
            self.ui.draw_obstacles(self.obstacles)
            self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
            self.ui.draw_snake(self.snake_list, self.ui.red)

            # Display target points above the Speed slider
            self.ui.display_text(f"Target Point: {self.target_score}", self.ui.width - 300, 30, self.ui.green, 15)

            # Display AI score below the Speed slider
            self.ui.display_text(f"AI: {self.score}", self.ui.width - 255, 150, self.ui.blue, 20)

            # Display timer below the AI score
            if timer_start:
                elapsed_time = (pygame.time.get_ticks() - timer_start) // 1000
                self.ui.display_text(f"Timer: {elapsed_time}s", self.ui.width - 275, 180, self.ui.white, 20)

            # Speed slider
            slider.draw(self.ui.screen, self.ui.default_font, "Speed", self.ui.gray, self.ui.red, self.ui.white)

            # Algorithm button
            algorithm_color = self.ui.red if dropdown_active else self.ui.white
            self.ui.display_text(dropdown_options[selected_algorithm_index] if not dropdown_active else "Algorithm",
                                 algorithm_button_rect.x + 10, algorithm_button_rect.y + 15, algorithm_color, 15)
            pygame.draw.rect(self.ui.screen, self.ui.light_red, algorithm_button_rect, 2)

            # Dropdown menu
            if dropdown_active:
                for i, option in enumerate(dropdown_options):
                    option_color = self.ui.red if i == selected_algorithm_index else self.ui.white
                    option_rect = pygame.Rect(self.ui.width - 280, 220 + (i+1) * 30, 210, 30)
                    pygame.draw.rect(self.ui.screen, self.ui.gray, option_rect)
                    self.ui.display_text(option, option_rect.x + 10, option_rect.y + 5, option_color, 10)

            # Start button
            start_color = self.ui.red if game_started else self.ui.white
            self.ui.display_text("Start", start_button_rect.x + 25, start_button_rect.y + 15, start_color, 20)
            pygame.draw.rect(self.ui.screen, self.ui.light_red, start_button_rect, 2)

            # Display Target Reached or Unreached message
            if target_reached and not end_message_displayed:
                message = "Target Reached!" if self.score >= self.target_score else "Target Unreached!"
                color = self.ui.red if self.score >= self.target_score else self.ui.white
                self.ui.display_text(message, start_button_rect.x, start_button_rect.y + 60, color, 20)
                pygame.display.flip()
                pygame.time.delay(6000)  # Delay for 6 seconds before exiting
                self.game_close = True  # Exit the game loop
                end_message_displayed = True

            self.ui.refresh_screen()
            self.clock.tick(self.snake_speed if game_started else 30)
            pygame.display.flip()

    # def update_screen_AI(self):
    #     self.ui.clear_screen()
    #     # Draw game elements
    #     self.ui.draw_grid()
    #     self.ui.draw_obstacles(self.obstacles)
    #     self.ui.draw_food((self.food_row, self.food_col), self.ui.light_red)
    #     self.ui.draw_snake(self.snake_list, self.ui.red)
    #
    #     # Display current score
    #     self.ui.display_text(f"AI: {self.score}", self.ui.width - 250, 10, self.ui.red, 20)
    #     # Display target score
    #     self.ui.display_text(f"Target: {self.target_score}", self.ui.width - 250, 40, self.ui.green, 20)
    #     # Display elapsed time
    #     if self.start_time:
    #         elapsed_time = int(pygame.time.get_ticks() / 1000) - self.start_time
    #         self.ui.display_text(f"Time: {elapsed_time}s", self.ui.width - 250, 70, self.ui.white, 20)
    #
    #     self.ui.refresh_screen()
