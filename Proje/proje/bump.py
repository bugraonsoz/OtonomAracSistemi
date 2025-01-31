import pygame

class Bump:
    def __init__(self, x, y, width, height, image_path, rotate=False, id=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.id = id  #ID EKLEMESİ
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
            if rotate:
                self.image = pygame.transform.rotate(self.image, 90)  #90 derece döndürme
        except pygame.error as e:
            print(f"Error loading image: {image_path}")
            raise e

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        #ID VARSA EKRANA YAZDIRMA
        if self.id is not None:
            font = pygame.font.Font(None, 20)
            text = font.render(f"ID: {self.id}", True, (255, 255, 255))
            screen.blit(text, (self.x, self.y - 15))  #15 birim yukarısına yazdırma
