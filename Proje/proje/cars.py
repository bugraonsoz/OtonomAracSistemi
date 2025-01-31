import pygame
from grid_map import MAP_X, MAP_Y, CELL_SIZE
from pathfinding import *
from Astar import AStar
from greedy import Greedy
from Bfs import Bfs
from Dijkstra import Dijkstra

class Car:
    def __init__(self, car_id, car_type, car_speed, car_image_path, car_location_x, car_location_y, pathfinder):
        self.car_id = car_id
        self.car_type = car_type
        self.car_speed = car_speed
        self.car_image_path = car_image_path
        self.car_image = pygame.image.load(car_image_path)
        self.car_location_x = car_location_x
        self.car_location_y = car_location_y
        self.pathfinder = pathfinder
        self.current_path = None
        self.path_index = 0
        
    def set_destination(self, goal_x: int, goal_y: int):
        """Set a new destination and calculate path"""
        # Convert pixel coordinates to grid coordinates
        start_grid_x = (self.car_location_x - MAP_X) // CELL_SIZE
        start_grid_y = (self.car_location_y - MAP_Y) // CELL_SIZE
        goal_grid_x = (goal_x - MAP_X) // CELL_SIZE
        goal_grid_y = (goal_y - MAP_Y) // CELL_SIZE
        

        print(f"\nSetting destination:")
        print(f"Start pixel coordinates: ({self.car_location_x}, {self.car_location_y})")
        print(f"Goal pixel coordinates: ({goal_x},{goal_y})")
        print(f"Start grid coordinates: ({start_grid_x},{start_grid_y})")
        print(f"Goal grid coordinates: ({goal_grid_x}, {goal_grid_y})")

        if isinstance(self.pathfinder, PathFinder):  # Handle DFS
            self.current_path = self.pathfinder.dfs(
                (start_grid_x, start_grid_y),
                (goal_grid_x, goal_grid_y)
            )
        elif isinstance(self.pathfinder, AStar):  # Handle AStar
            self.current_path = self.pathfinder.find_path(
                (start_grid_x, start_grid_y),
                (goal_grid_x, goal_grid_y)
            )
        elif isinstance(self.pathfinder, Greedy):  # Handle Greedy
            self.current_path = self.pathfinder.find_path(
                (start_grid_x, start_grid_y),
                (goal_grid_x, goal_grid_y)
            )
        elif isinstance(self.pathfinder, Bfs):  # Handle Bfs
            self.current_path = self.pathfinder.find_path(
                (start_grid_x, start_grid_y),
                (goal_grid_x, goal_grid_y)
            )
        elif isinstance(self.pathfinder, Dijkstra):  # Handle Dijkstra
            self.current_path = self.pathfinder.find_path(
                (start_grid_x, start_grid_y),
                (goal_grid_x, goal_grid_y)
            )
        else:
            print("Unsupported pathfinding algorithm.")
            self.current_path = None

        if self.current_path:
            print("\nConverting grid path to pixel coordinates:")
            self.current_path = [
                (x * CELL_SIZE + MAP_X, y * CELL_SIZE + MAP_Y)
                for x, y in self.current_path
            ]
            print(f"Pixel path: {self.current_path}")
        else:
            print("No path found!")

        self.path_index = 0

        
    def update(self, delta_time):
        """Update car position based on current path"""
        if not self.current_path or self.path_index >= len(self.current_path):
            return
        
        next_pos = self.current_path[self.path_index]
        
        # Yaya kontrolü - Aracın önündeki yaya geçidini kontrol et
        current_grid_x = (self.car_location_x - MAP_X) // CELL_SIZE
        current_grid_y = (self.car_location_y - MAP_Y) // CELL_SIZE
        next_grid_x = (next_pos[0] - MAP_X) // CELL_SIZE
        next_grid_y = (next_pos[1] - MAP_Y) // CELL_SIZE
        
        # Yaya geçidi kontrolü
        for ped in self.pathfinder.pedestrians:
            if ped.state == "full" and ped.is_crossing():
                # Yaya geçidi koordinatlarını kontrol et
                crossing_coords = [(x, y) for x, y in [ped.path_start, ped.path_end]]
                
                # Aracın şu anki ve bir sonraki konumu yaya geçidinde mi kontrol et
                current_in_crossing = (current_grid_x, current_grid_y) in crossing_coords
                next_in_crossing = (next_grid_x, next_grid_y) in crossing_coords
                
                # Eğer araç yaya geçidine yaklaşıyorsa veya geçitte ise dur
                if current_in_crossing or next_in_crossing:
                    print(f"Car stopped for pedestrian at crossing")
                    return
        
        print(f"\nCurrent car position: ({self.car_location_x}, {self.car_location_y})")
        print(f"Moving towards: {next_pos}")
        
        # Grid koordinatlarına çevir
        current_grid_x = (self.car_location_x - MAP_X) // CELL_SIZE
        current_grid_y = (self.car_location_y - MAP_Y) // CELL_SIZE
        
        # Hız faktörünü hesapla
        speed_factor = 1.0 / self.pathfinder.get_cost(current_grid_x, current_grid_y)
        base_speed = 5
        adjusted_speed = max(0.5, base_speed * speed_factor)  # Minimum hız 0.5
        
        print(f"Speed factor: {speed_factor:.2f}, Adjusted speed: {adjusted_speed:.2f}")
        
        # Hareket yönünü hesapla
        dx = next_pos[0] - self.car_location_x
        dy = next_pos[1] - self.car_location_y
        
        # Aracın yönünü belirle ve resmi döndür
        if abs(dx) > abs(dy):  # Yatay hareket
            if dx > 0:  # Sağa
                self.car_image = pygame.transform.rotate(pygame.image.load(self.car_image_path), 0)
            else:  # Sola
                self.car_image = pygame.transform.rotate(pygame.image.load(self.car_image_path), 180)
        else:  # Dikey hareket
            if dy > 0:  # Aşağı
                self.car_image = pygame.transform.rotate(pygame.image.load(self.car_image_path), -90)
            else:  # Yukarı
                self.car_image = pygame.transform.rotate(pygame.image.load(self.car_image_path), 90)
        
        # X koordinatında hareket
        if self.car_location_x < next_pos[0]:
            self.car_location_x += adjusted_speed
        elif self.car_location_x > next_pos[0]:
            self.car_location_x -= adjusted_speed
        
        # Y koordinatında hareket
        if self.car_location_y < next_pos[1]:
            self.car_location_y += adjusted_speed
        elif self.car_location_y > next_pos[1]:
            self.car_location_y -= adjusted_speed
        
        # Hedefe yeterince yakınsa bir sonraki noktaya geç
        if (abs(self.car_location_x - next_pos[0]) < adjusted_speed and 
            abs(self.car_location_y - next_pos[1]) < adjusted_speed):
            self.car_location_x = next_pos[0]
            self.car_location_y = next_pos[1]
            self.path_index += 1
            print(f"Reached waypoint {self.path_index-1}, moving to next")
    
    def draw(self, screen):
        """Draw the car on the screen"""
        screen.blit(self.car_image, (self.car_location_x, self.car_location_y))


