import pygame  # Pygame kütüphanesi dahil edildi

# --- Uygulama Ayarları ---
APP_WIDTH = 1100  # Uygulama genişliği
APP_HEIGHT = 750  # Uygulama yüksekliği
APP_BACKGROUND_COLOR = (193, 181, 154)  # Arka plan rengi (#c1b59a)

# --- Harita ve Izgara Ayarları ---
GRID_SIZE = 20
CELL_SIZE = 35  # Her hücrenin boyutu (piksel cinsinden)
MAP_WIDTH = 700
MAP_HEIGHT = 700
MAP_X, MAP_Y = 200, 25  # Haritanın başlangıç koordinatları (piksel cinsinden)

# --- Renk Ayarları ---
GRID_COLOR = (200, 200, 200)  # Izgara çizgilerinin rengi
TEXT_COLOR = (0, 0, 0)        # Metinlerin rengi

# --- Yol Koordinatları ---
road_coordinates = [
    (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2), (16, 2),
    (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3), (15, 3), (16, 3),
    (3, 4), (4, 4), (10, 4), (11, 4), (17, 4), (18, 4),
    (3, 5), (4, 5), (10, 5), (11, 5), (17, 5), (18, 5),
    (3, 6), (4, 6), (10, 6), (11, 6), (17, 6), (18, 6),
    (3, 7), (4, 7), (10, 7), (11, 7), (17, 7), (18, 7),
    (3, 8), (4, 8), (10, 8), (11, 8), (17, 8), (18, 8),
    (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9), (18, 9),
    (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10),
    (3, 11), (4, 11), (10, 11), (11, 11), (17, 11), (18, 11),
    (3, 12), (4, 12), (10, 12), (11, 12), (17, 12), (18, 12),
    (3, 13), (4, 13), (10, 13), (11, 13), (17, 13), (18, 13),
    (3, 14), (4, 14), (10, 14), (11, 14), (17, 14), (18, 14),
    (3, 15), (4, 15), (10, 15), (11, 15), (17, 15), (18, 15),
    (2, 16), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (17, 16), (18, 16),
    (2, 17), (3, 17), (4, 17), (5, 17), (6, 17), (7, 17), (8, 17), (9, 17), (10, 17), (11, 17), (12, 17), (13, 17), (14, 17), (15, 17), (16, 17), (17, 17), (18, 17),
]

# --- Izgara Koordinatlarını Piksel Koordinatlarına Çeviren Fonksiyonlar ---
def Road_x(grid_x):
    """
    Izgaradaki x koordinatını piksel koordinatına çevir.
    :param grid_x: Izgaradaki x koordinatı (örneğin, 16).
    :return: Piksel x koordinatı.
    """
    return grid_x * CELL_SIZE + MAP_X


def Road_y(grid_y):
    """
    Izgaradaki y koordinatını piksel koordinatına çevir.
    :param grid_y: Izgaradaki y koordinatı (örneğin, 2).
    :return: Piksel y koordinatı.
    """
    return grid_y * CELL_SIZE + MAP_Y


# --- Harita Boyutlarını Döndüren Fonksiyonlar ---
def get_map_dimensions():
    """
    Harita boyutlarını döndür (genişlik ve yükseklik).
    """
    return MAP_WIDTH, MAP_HEIGHT


def get_cell_size():
    """
    Her hücrenin boyutunu döndür.
    """
    return CELL_SIZE


# --- Izgarayı Çizen Fonksiyon ---
def draw_grid(screen, font, map_x, map_y):
    """
    Izgarayı ve sıraları/sütunları numaraları ile birlikte çizer.
    """
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Hücrenin koordinatları
            x = map_x + col * CELL_SIZE
            y = map_y + row * CELL_SIZE

            # Izgarayı çiz
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRID_COLOR, rect, 1)

            # İlk sıra veya sütun için siyah arka plan ve beyaz metin
            if row == 0 or col == 0:
                pygame.draw.rect(screen, (0, 0, 0), rect)

                # Sütun numaralarını çiz
                if row == 0:
                    text = font.render(str(col), True, (255, 255, 255))  # Beyaz metin
                # Satır numaralarını çiz
                elif col == 0:
                    text = font.render(str(row), True, (255, 255, 255))  # Beyaz metin

                # Metni hücrenin ortasına yerleştir
                text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                screen.blit(text, text_rect)
