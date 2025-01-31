import pygame
import random

# Hava durumu durumlarını tanımla
weather_states = ["Sunny", "Rainy", "Foggy"]
current_weather = "Sunny"
button_pressed = [False, False, False]  # Track pressed state of each button
MAP_X, MAP_Y = 200, 25 # Map offset for drawing

# Etkiler için renk tanımları
RAIN_COLOR = pygame.Color(0, 0, 255, 128)  # Yağmurlu hava için yarı saydam mavi
FOG_COLOR = pygame.Color(255, 255, 255, 128)  # Sisli hava için yarı saydam beyaz

# Yağmur animasyonu için ayar
raindrops = [[random.randint(0, 700), random.randint(0, 700)] for _ in range(50)] # 50 adet rastgele konumlu yağmur damlası başlat

# Hava durumu etkilerini uygula (yağmur için konum düzeltmesiyle birlikte)

def apply_weather_effects(screen):
    global current_weather
    if current_weather == "Rainy":
        for drop in raindrops:
            # Yağmurluysa: Her damla için çizgi çizer ve konumunu günceller
            pygame.draw.line(screen, RAIN_COLOR, 
                             (drop[0] + MAP_X, drop[1] + MAP_Y), 
                             (drop[0] + MAP_X, drop[1] + MAP_Y + 5), 2)
            drop[1] += 5  
            
            if drop[1] > 700:
                drop[1] = random.randint(25, 690)  # Keep it within screen height
                drop[0] = random.randint(25, 700)  # Keep it within screen width
    # Sisliyse: Yarı saydam beyaz bir katman ekler
    elif current_weather == "Foggy":
        fog_overlay = pygame.Surface((700, 700), pygame.SRCALPHA)
        fog_overlay.fill(FOG_COLOR)
        screen.blit(fog_overlay, (MAP_X, MAP_Y))
# Düğme tıklamalarını işleyen fonksiyon
# Tıklanan düğmeye göre hava durumu durumunu ayarlar
def check_button_press(pos):
    global button_pressed, current_weather
    button_width, button_height = 90, 35
    button_x, button_y = 30, 50
    button_gap = 10

    for i in range(len(weather_states)):
        rect = pygame.Rect(button_x, button_y + i * (button_height + button_gap), button_width, button_height)
        if rect.collidepoint(pos):
            button_pressed = [False] * len(weather_states)  
            button_pressed[i] = True  
            current_weather = weather_states[i]  

# Düğmeleri çizme fonksiyonu
# Her hava durumu için düğmeleri çizer ve durumuna göre renk ayarlar

def draw_buttons(screen):
    button_width, button_height = 90, 35
    button_x, button_y = 30, 50
    button_gap = 10
    button_text_color = pygame.Color("black")

    for i, weather in enumerate(weather_states):
        rect = pygame.Rect(button_x, button_y + i * (button_height + button_gap), button_width, button_height)

        # Düğmeye basılıp basılmadığına göre rengi belirleyen koşul
        button_color = pygame.Color("#d885f9") if button_pressed[i] else pygame.Color("#FFFFFF")

        pygame.draw.rect(screen, button_color, rect)
        font = pygame.font.SysFont(None, 24)
        text = font.render(weather, True, button_text_color)
        screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))


       
#!!!!!!!!Aşağıdaki fonksiyon sadece açıklama amaçlı yazılmıştır ve şu anda çalışmıyor

# Arabaya varsayılan hız tanımla (şimdilik devre dışı bırakılmış bir özellik)
# Arabanın varsayılan hızı 5
original_car_speed = 5  
current_car_speed = original_car_speed  

# Hava durumuna göre araba hızını değiştirme fonksiyonu
# Yağmurlu: Hız %20 azalır
# Sisli: Hız %40 azalır
# Güneşli: Hız eski haline döner

def adjust_car_speed():
    global current_car_speed
    if current_weather == "Rainy":
        current_car_speed = original_car_speed * 0.8  
    elif current_weather == "Foggy":
        current_car_speed = original_car_speed * 0.6  
    elif current_weather == "Sunny":
        current_car_speed = original_car_speed  

