import pygame

class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val):
        self.x = x
        self.y = y
        self.width = width
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.handle_radius = 10
        self.bar_height = 4
        self.handle_x = x + (width * (initial_val - min_val) / (max_val - min_val))
        self.dragging = False

    def draw(self, screen, font, label, color_bar, color_handle, color_text):
        # Draw the slider bar
        pygame.draw.rect(screen, color_bar, (self.x, self.y, self.width, self.bar_height))

        # Draw the handle
        pygame.draw.circle(screen, color_handle, (int(self.handle_x), self.y + self.bar_height // 2), self.handle_radius)

        # Display the value as text
        value_text = font.render(f"{int(self.value)}", True, color_text)
        screen.blit(value_text, (self.x + self.width + 50, self.y - 10))

        # Display the label
        label_text = font.render(label, True, color_text)
        screen.blit(label_text, (self.x - 110, self.y - 10))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if abs(mouse_x - self.handle_x) <= self.handle_radius and abs(mouse_y - (self.y + self.bar_height // 2)) <= self.handle_radius:
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x = event.pos[0]
            self.handle_x = max(self.x, min(self.x + self.width, mouse_x))
            self.value = max(self.min_val,
                             self.min_val + (self.max_val - self.min_val) * ((self.handle_x - self.x) / self.width))

