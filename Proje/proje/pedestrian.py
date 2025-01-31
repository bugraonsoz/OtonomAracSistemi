# pedestrian.py

import pygame
import random
import os

class Pedestrian:
    def __init__(self, ped_id, path_start, path_end, cell_size, map_x, map_y, rotate=False):
           
        """
        Yaya tanımı.
        :param ped_id: Yayanın kimliği.
        :param path_start: Başlangıç koordinatları (tuple) (x1, y1).
        :param path_end: Bitiş koordinatları (tuple) (x2, y2).
        :param cell_size: Hücre boyutu.
        :param map_x: Haritanın X eksenindeki kaydırması.
        :param map_y: Haritanın Y eksenindeki kaydırması.
        :param rotate: True ise yol ve yaya görüntüsünü 90 derece döndür.

        """

        self.ped_id = ped_id
        self.path_start = path_start  # tuple (x1, y1)
        self.path_end = path_end      # tuple (x2, y2)
        self.cell_size = cell_size
        self.map_x = map_x
        self.map_y = map_y
        self.rotate = rotate

         # Yol ve yaya görüntülerini yükle
        self.path_image = pygame.image.load(os.path.join("images", "pedestrian", "1.png"))
        self.path_image = pygame.transform.scale(self.path_image, (35, 35))
        
        self.person_image = pygame.image.load(os.path.join("images", "person", "1.png"))
        self.person_image = pygame.transform.scale(self.person_image, (35, 35))
        
        # Yol döndürme gerekiyorsa görüntüleri döndür
        if self.rotate:
            self.path_image = pygame.transform.rotate(self.path_image, 90)
            self.person_image = pygame.transform.rotate(self.person_image, 90)
        
       # Yolun durumu
        self.state = "empty"  # "empty" أو "full"
        
        # Yayanın mevcut konumunu ayarla
        self.current_position = None
        self.target_position = None
        self.direction = None
        self.speed = 20  # Saniyede piksel (hız azaltıldı)
        
        # Yeni yaya oluşturmak için zamanlayıcı ayarla
        self.reset_timer()
        
    def reset_timer(self):
        """
        Yeni yaya oluşturmak için zamanlayıcıyı sıfırla.
        """
        self.timer = random.randint(3, 10)
        
    def update(self, delta_time):
        """
        Yayanın durumunu güncelle.
        :param delta_time: Son güncellemeden itibaren geçen süre.
        """
        if self.state == "empty":
            self.timer -= delta_time
            if self.timer <= 0:
                self.generate_pedestrian()
        elif self.state == "full":
            # Hareket eden yayanın konumunu güncelle
            self.current_position[0] += self.direction[0] * self.speed * delta_time
            self.current_position[1] += self.direction[1] * self.speed * delta_time
            
            # Yayanın hedefe ulaşıp ulaşmadığını kontrol et
            reached = False
            if self.direction[0] > 0 and self.current_position[0] >= self.target_position[0]:
                reached = True
            elif self.direction[0] < 0 and self.current_position[0] <= self.target_position[0]:
                reached = True
            if self.direction[1] > 0 and self.current_position[1] >= self.target_position[1]:
                reached = True
            elif self.direction[1] < 0 and self.current_position[1] <= self.target_position[1]:
                reached = True

            if reached:
                self.state = "empty"
                self.reset_timer()
                
    def generate_pedestrian(self):
        """
        Yeni bir yaya oluştur ve yolu dolu yap.
        """
        self.state = "full"
        # Başlangıç ve bitiş konumlarını piksel cinsinden ayarla
        start_x = self.map_x + self.path_start[0] * self.cell_size
        start_y = self.map_y + self.path_start[1] * self.cell_size
        end_x = self.map_x + self.path_end[0] * self.cell_size
        end_y = self.map_y + self.path_end[1] * self.cell_size
        
        self.current_position = [start_x, start_y]
        self.target_position = [end_x, end_y]
        
        # Hareket yönünü hesapla
        dx = self.target_position[0] - self.current_position[0]
        dy = self.target_position[1] - self.current_position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            self.direction = [dx / distance, dy / distance]
        else:
            self.direction = [0, 0]
        
    def draw(self, screen):
        """
        Yol ve hareket eden yayayı çiz.
        :param screen: Çizim ekranı.
        """
        # Yol görüntüsünü (her yol parçası için kare) çiz
        for path in [self.path_start, self.path_end]:
            path_x = self.map_x + path[0] * self.cell_size
            path_y = self.map_y + path[1] * self.cell_size
            screen.blit(self.path_image, (path_x, path_y))
        
        # Yolu doluysa yayayı çiz
        if self.state == "full" and self.current_position:
            screen.blit(self.person_image, (self.current_position[0], self.current_position[1]))

    def is_crossing(self) -> bool:
        """Yayanın yoldan geçip geçmediğini kontrol et"""
        # Yayanın şu anki konumu ile başlangıç ve bitiş noktaları arasındaki mesafeyi kontrol et
        start_x = self.path_start[0] * self.cell_size + self.map_x
        start_y = self.path_start[1] * self.cell_size + self.map_y
        end_x = self.path_end[0] * self.cell_size + self.map_x
        end_y = self.path_end[1] * self.cell_size + self.map_y
        
        # Eğer yaya başlangıç ve bitiş noktaları arasındaysa geçiyor demektir
        is_between_x = min(start_x, end_x) <= self.current_position[0] <= max(start_x, end_x)
        is_between_y = min(start_y, end_y) <= self.current_position[1] <= max(start_y, end_y)
        
        return is_between_x and is_between_y
