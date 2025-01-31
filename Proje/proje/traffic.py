import pygame
import random

class TrafficSignal:
    def __init__(self, signal_id, x, y, width, height, image_path, rotate=False, timer_box_offset=(0, 0), effect_area=None):
        self.signal_id = signal_id
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        if rotate:
            self.image = pygame.transform.rotate(self.image, 90)

        self.timer_box_offset = timer_box_offset

        # Rastgele başlangıç durumu ve süreler
        self.state = random.choice(["red", "green"])
        self.shared_time = random.randint(10, 15)  # Rastgele 10-15 saniye arası süre
        self.time_left = self.shared_time

        self.paired_signal = None
        self.is_primary = False

        # Etrafındaki etkilediği alan
        self.effect_area = effect_area or []

    def set_effect_area(self, coordinates: list):
        """
        Trafik ışığının etkilediği alanı ayarlar.
        """
        self.effect_area = coordinates

    def is_within_effect_area(self, grid_x, grid_y):
        """
        Verilen hücrenin trafik ışığının etkilediği alanda olup olmadığını kontrol eder.
        """
        return (grid_x, grid_y) in self.effect_area

    def set_pair(self, other_signal, is_primary=False):
        self.paired_signal = other_signal
        other_signal.paired_signal = self
        self.is_primary = is_primary
        other_signal.is_primary = not is_primary

        if self.is_primary:
            self.time_left = self.shared_time
            other_signal.time_left = self.shared_time
        else:
            self.time_left = other_signal.time_left

    def update(self, delta_time):
        self.time_left -= delta_time
        if self.time_left <= 0:
            self.toggle_state()
            self.shared_time = random.randint(10, 15)  # Her geçişte rastgele süre belirle
            self.time_left = self.shared_time
            if self.paired_signal:
                self.paired_signal.toggle_state()
                self.paired_signal.shared_time = self.shared_time
                self.paired_signal.time_left = self.shared_time

    def toggle_state(self):
        self.state = "green" if self.state == "red" else "red"

    def draw(self, screen, font, cell_size):
        screen.blit(self.image, (self.x, self.y))
        color = (255, 0, 0) if self.state == "red" else (0, 128, 0)
        rect_x = self.x + self.timer_box_offset[0] * cell_size
        rect_y = self.y + self.timer_box_offset[1] * cell_size
        rect_size = cell_size
        pygame.draw.rect(screen, color, (rect_x, rect_y, rect_size, rect_size))
        text_color = (255, 255, 255)
        text = font.render(str(max(0, int(self.time_left))), True, text_color)
        text_rect = text.get_rect(center=(rect_x + rect_size // 2, rect_y + rect_size // 2))
        screen.blit(text, text_rect)

    def is_red(self):
        return self.state == "red"

    def is_near(self, car, threshold=50):
        distance = ((self.x - car.car_location_x) ** 2 + (self.y - car.car_location_y) ** 2) ** 0.5
        return distance < threshold