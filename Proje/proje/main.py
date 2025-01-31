# --- Adjusted Main ---
from Dijkstra import Dijkstra
import pygame
import os
import random

from grid_map import get_map_dimensions, get_cell_size, draw_grid, Road_x, Road_y, road_coordinates, APP_WIDTH, APP_HEIGHT, APP_BACKGROUND_COLOR
from traffic import TrafficSignal 
from pedestrian import Pedestrian
from bump import Bump
from weather import apply_weather_effects, check_button_press, draw_buttons
from cars import Car
from pathfinding import PathFinder
from Astar import AStar
from button import Button
from greedy import Greedy
from Bfs import Bfs

# --- Pygame Settings ---
pygame.init()
screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
pygame.display.set_caption("YAPAY ZEKA")
font = pygame.font.Font(None, 30)

# --- Map and Grid Settings ---
MAP_WIDTH, MAP_HEIGHT = get_map_dimensions()
CELL_SIZE = get_cell_size()
MAP_X, MAP_Y = 200, 25

# --- Load Map Image ---
map_image_path = os.path.join("images", "road", "1.png")
map_image = pygame.image.load(map_image_path)
map_image = pygame.transform.scale(map_image, (MAP_WIDTH, MAP_HEIGHT))

# --- Traffic Signals ---
signals = []
signal_pairs = [
    (9, 4, True), (12, 4, False), (9, 8, True), (12, 11, False), (16, 8, True), (16, 11, False)
]
for idx, (x, y, rotate) in enumerate(signal_pairs, start=1):
    signals.append(TrafficSignal(idx, MAP_X + x * CELL_SIZE, MAP_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE, "images/traffic/1.png", rotate=rotate))
    
for i in range(0, len(signals), 2):
    signals[i].set_pair(signals[i + 1], is_primary=True)



# --- Bumps Setup ---
bumps = []
rotation_bump_coords = [(6, 2), (6, 3),(14, 9), (14, 10), (14, 16), (14, 17)]
bump_coordinates = [
    [(6, 2), (6, 3)], [(17, 6), (18, 6)], [(14, 9), (14, 10)], [(3, 13), (4, 13)], [(10, 13), (11, 13)], [(14, 16), (14, 17)]
]
selected_bump_locations = random.sample(bump_coordinates, 3)
for location in selected_bump_locations:
    for x, y in location:
        rotate = (x, y) in rotation_bump_coords
        bumps.append(Bump(
            x=MAP_X + x * CELL_SIZE,
            y=MAP_Y + y * CELL_SIZE,
            width=CELL_SIZE,
            height=CELL_SIZE,
            image_path="images/bump/1.png",
            rotate=rotate
        ))

# --- Pedestrian Paths ---
all_pedestrian_paths = [
    ((14, 2), (14, 3)), ((7, 9), (7, 10)), ((3, 6), (4, 6)), ((7, 16), (7, 17)), ((17, 13), (18, 13)), ((10, 6), (11, 6))
]
selected_pedestrian_paths = random.sample(all_pedestrian_paths, 3)

pedestrians = []
for idx, path in enumerate(selected_pedestrian_paths):
    path_start, path_end = path
    rotate = path in [
        ((3, 6), (4, 6)), ((17, 13), (18, 13)), ((10, 6), (11, 6))
    ]
    pedestrians.append(Pedestrian(
        ped_id=idx + 1,
        path_start=path_start,
        path_end=path_end,
        cell_size=CELL_SIZE,
        map_x=MAP_X,
        map_y=MAP_Y,
        rotate=rotate
    ))

# --- Cars Setup ---
pathfinder = PathFinder(road_coordinates, signals, bumps, pedestrians)
car1 = Car(
    car_id=1,
    car_type="DFS",
    car_speed=2,
    car_image_path="images/cars/1.png",
    car_location_x=Road_x(2),
    car_location_y=Road_y(16),
    pathfinder=pathfinder
)

astar_pathfinder = AStar(road_coordinates, signals, bumps, pedestrians)
car2 = Car(
    car_id=2,
    car_type="AStar",
    car_speed=2,
    car_image_path="images/cars/2.png",
    car_location_x=Road_x(2),
    car_location_y=Road_y(16),
    pathfinder=astar_pathfinder
)

greedy_pathfinder= Greedy(road_coordinates,signals,bumps,pedestrians)
car3 = Car(
    car_id=3,
    car_type="Greedy",
    car_speed=2,
    car_image_path="images/cars/3.png",
    car_location_x=Road_x(2),
    car_location_y=Road_y(16),
    pathfinder=greedy_pathfinder
)

bfs_pathfinder= Bfs(road_coordinates,signals,bumps,pedestrians)
car4 = Car(
    car_id=4,
    car_type="Bfs",
    car_speed=2,
    car_image_path="images/cars/4.png",
    car_location_x=Road_x(2),
    car_location_y=Road_y(16),
    pathfinder=bfs_pathfinder
)

dijkstra_pathfinder= Dijkstra(road_coordinates,signals,bumps,pedestrians)
car5 = Car(
    car_id=5,
    car_type="Dijkstra",
    car_speed=2,
    car_image_path="images/cars/5.png",
    car_location_x=Road_x(2),
    car_location_y=Road_y(16),
    pathfinder=dijkstra_pathfinder
)

signal_coordinates = [
    [(9, 2), (9, 3)],
    [(9, 9), (9, 10)],
    [(10, 4), (11, 4)],
    [(10, 11), (11, 11)],
    [(16, 9), (16, 10)],
    [(17, 11), (18, 11)],
]

signals = [
    TrafficSignal(
        signal_id=1,
        x=MAP_X + 9 * CELL_SIZE,
        y=MAP_Y + 4 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(9, 2), (9, 3)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=2,
        x=MAP_X + 12 * CELL_SIZE,
        y=MAP_Y + 4 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(10, 4), (11, 4)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=3,
        x=MAP_X + 9 * CELL_SIZE,
        y=MAP_Y + 8 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(9, 9), (9, 10)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=4,
        x=MAP_X + 12 * CELL_SIZE,
        y=MAP_Y + 11 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(10, 11), (11, 11)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=5,
        x=MAP_X + 16 * CELL_SIZE,
        y=MAP_Y + 8 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(16, 9), (16, 10)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=6,
        x=MAP_X + 16 * CELL_SIZE,
        y=MAP_Y + 11 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(17, 11), (18, 11)]  # Bu ışığın etki ettiği alan
    ),
    TrafficSignal(
        signal_id=7,
        x=MAP_X + 2 * CELL_SIZE,
        y=MAP_Y + 11 * CELL_SIZE,
        width=CELL_SIZE,
        height=CELL_SIZE,
        image_path="images/traffic/1.png",
        effect_area=[(3, 11), (4, 11)]  # Bu ışığın etki ettiği alan
    )
]

# --- Buttons ---
dfs_button = Button(x=10, y=APP_HEIGHT - 60, width=100, height=40, text="DFS", color=(200, 200, 200), hover_color=(180, 180, 180))
astar_button = Button(x=10, y=APP_HEIGHT - 105, width=100, height=40, text="AStar", color=(200, 200, 200), hover_color=(180, 180, 180))
greedy_button = Button(x=10, y=APP_HEIGHT - 150, width=100, height=40, text="Greedy", color=(200, 200, 200), hover_color=(180, 180, 180))
bfs_button = Button(x=10, y=APP_HEIGHT - 195, width=100, height=40, text="BFS", color=(200, 200, 200), hover_color=(180, 180, 180))
dijkstra_button = Button(x=10, y=APP_HEIGHT - 240, width=100, height=40, text="Dijkstra", color=(200, 200, 200), hover_color=(180, 180, 180))

# --- Main Loop Variables ---
is_paused = False
car_moving = False
selected_algorithm = None

# --- Pause Toggle ---
def toggle_pause():
    global is_paused
    is_paused = not is_paused


   # Bekleme süresi ve hareket durumu değişkenleri
wait_times = [0, 0, 0, 0, 0]
car_moving = [False, False, False, False, False]




def is_near_red_signal(car, signals):
    car_grid_x = (car.car_location_x - MAP_X) // CELL_SIZE
    car_grid_y = (car.car_location_y - MAP_Y) // CELL_SIZE

    for signal in signals:
        if signal.is_red() and signal.is_within_effect_area(car_grid_x, car_grid_y):
            return signal
    return None
def update_car(car, delta_time, car_index):
    """
    Arabayı güncelle ve trafik ışığı durumunu kontrol et.
    """
    if car_moving[car_index]: 
        red_signal = is_near_red_signal(car, signals)  # Yakın bir kırmızı ışık var mı?
        if red_signal:  # Eğer kırmızı ışık varsa araba bekler
            print(f"Car{car_index + 1} is waiting for the traffic light to turn green.")
            car_moving[car_index] = False
            wait_times[car_index] = red_signal.time_left
        else:  # Kırmızı ışık yoksa araba hareket eder
            car.update(delta_time)
            if not car.current_path or car.path_index >= len(car.current_path):
                car_moving[car_index] = False
    for i in range(5):
        if not car_moving[i] and wait_times[i] > 0:
            wait_times[i] -= delta_time
            if wait_times[i] <= 0:
                car_moving[i] = True

# --- Main Game Loop ---
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()

        if dfs_button.handle_event(event):
            selected_algorithm = "DFS"
            car1.set_destination(Road_x(16), Road_y(2))
            car_moving[0] = True
            print("DFS selected and car1 destination set.")

        if astar_button.handle_event(event):
            selected_algorithm = "AStar"
            car2.set_destination(Road_x(16), Road_y(2))
            car_moving[1] = True
            print("AStar selected and car2 destination set.")

        if greedy_button.handle_event(event):
            selected_algorithm = "Greedy"
            car3.set_destination(Road_x(16), Road_y(2))
            car_moving[2] = True
            print("Greedy selected and car3 destination set.")
        
        if bfs_button.handle_event(event):
            selected_algorithm = "BFS"
            car4.set_destination(Road_x(16), Road_y(2))
            car_moving[3] = True
            print("BFS selected and car4 destination set.")
            
        if dijkstra_button.handle_event(event):
            selected_algorithm = "Dijkstra"
            car5.set_destination(Road_x(16), Road_y(2))
            car_moving[4] = True
            print("Dijkstra selected and car5 destination set.")

    if is_paused:
        screen.fill(APP_BACKGROUND_COLOR)
        screen.blit(map_image, (MAP_X, MAP_Y))
        draw_grid(screen, font, MAP_X, MAP_Y)
        car1.draw(screen)
        car2.draw(screen)
        car3.draw(screen)
        car4.draw(screen)
        car5.draw(screen)

        for signal in signals:
            signal.draw(screen, font, CELL_SIZE)
        for bump in bumps:
            bump.draw(screen)
        for ped in pedestrians:
            ped.draw(screen)

        dfs_button.draw(screen, font)
        astar_button.draw(screen, font)
        greedy_button.draw(screen,font)
        bfs_button.draw(screen,font)
        dijkstra_button.draw(screen,font)
        pygame.display.flip()
        clock.tick(60)
        continue

    delta_time = clock.tick(60) / 1000.0

    screen.fill(APP_BACKGROUND_COLOR)
    screen.blit(map_image, (MAP_X, MAP_Y))
    draw_grid(screen, font, MAP_X, MAP_Y)
    apply_weather_effects(screen)

    for signal in signals:
        signal.update(delta_time)
        signal.draw(screen, font, CELL_SIZE)

    for bump in bumps:
        bump.draw(screen)

    for ped in pedestrians:
        ped.update(delta_time)
        ped.draw(screen)

    # Arabaları güncelle
    update_car(car1, delta_time, 0)
    update_car(car2, delta_time, 1)
    update_car(car3, delta_time, 2)
    update_car(car4, delta_time, 3)
    update_car(car5, delta_time, 4)

    # Bekleme sürelerini kontrol et ve süre dolduğunda hareketi başlat
    for i in range(5):
        if not car_moving[i] and wait_times[i] > 0:
            wait_times[i] -= delta_time
            if wait_times[i] <= 0:
                car_moving[i] = True

    car1.draw(screen)
    car2.draw(screen)
    car3.draw(screen)
    car4.draw(screen)
    car5.draw(screen)

    dfs_button.draw(screen, font)
    astar_button.draw(screen, font)
    greedy_button.draw(screen, font)
    bfs_button.draw(screen, font)
    dijkstra_button.draw(screen,font)
    pygame.display.flip()

pygame.quit()