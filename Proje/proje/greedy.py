import heapq,math
from typing import List, Tuple, Optional
from dataclasses import dataclass
from grid_map import Road_x, Road_y, MAP_X, MAP_Y, CELL_SIZE

@dataclass(order=True)
class Node:
    f_cost: float = float("inf")  # Total cost for priority queue ordering
    x: int = 0  # Grid x-coordinate
    y: int = 0  # Grid y-coordinate
    h_cost: float = float("inf")  # Heuristic cost (estimated cost to goal)
    parent: Optional['Node'] = None  # Parent node for path reconstruction

    def __post_init__(self):
        # Automatically calculate f_cost as g_cost + h_cost
        self.f_cost = self.h_cost

class Greedy:
    def __init__(self, road_coordinates: List[Tuple[int, int]], signals, bumps, pedestrians):
        self.road_coordinates = set(road_coordinates)  # Valid road coordinates
        self.signals = signals
        self.bumps = bumps
        self.pedestrians = pedestrians
        print("AStar initialized with road coordinates:", sorted(self.road_coordinates))

    def heuristic(self, start: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """Calculate Manhattan distance heuristic."""
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def is_valid_move(self, position: Tuple[int, int]) -> bool:
        if position not in self.road_coordinates:
            return False

        for signal in self.signals:
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if (position == (signal_grid_x, signal_grid_y)) and signal.state == "red":
                return False

        for ped in self.pedestrians:
            ped_grid_x = (ped.current_position[0] - MAP_X) // CELL_SIZE if ped.current_position else None
            ped_grid_y = (ped.current_position[1] - MAP_Y) // CELL_SIZE if ped.current_position else None
            if position == (ped_grid_x, ped_grid_y) and ped.is_crossing():
                return False

        return True
    def get_neighbors(self, node: Node) -> List[Node]:
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Cardinal directions

        for dx, dy in directions:
            new_x, new_y = node.x + dx, node.y + dy
            if self.is_valid_move((new_x, new_y)):
                neighbors.append(Node(x=new_x, y=new_y))
        return neighbors
    
    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """Greedy  algoritmasını kullanarak yol bul."""
        if start not in self.road_coordinates or goal not in self.road_coordinates:
            print(f"Start {start} veya goal {goal} yol üzerinde değil.")
            return None

        open_set = []
        closed_set = set()

        start_node = Node(x=start[0], y=start[1], h_cost=self.heuristic(start, goal))
        heapq.heappush(open_set, (start_node.f_cost, start_node))

        while open_set:
            current_node = heapq.heappop(open_set)[1]

            if (current_node.x, current_node.y) == goal:
                path = []
                while current_node:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]  # Başlangıçtan hedefe doğru yolu döndür

            closed_set.add((current_node.x, current_node.y))

            for neighbor in self.get_neighbors(current_node):
                neighbor_coords = (neighbor.x, neighbor.y)

                if neighbor_coords in closed_set:
                    continue
            
                tentative_g_cost = current_node.h_cost + self.get_cost(neighbor.x, neighbor.y)

                if tentative_g_cost < neighbor.h_cost:
                    neighbor.h_cost = tentative_g_cost
                    neighbor.h_cost = self.heuristic((neighbor.x, neighbor.y), goal)
                    neighbor.parent = current_node

                    if not any(neighbor_coords == (n.x, n.y) for _, n in open_set):
                        heapq.heappush(open_set, (neighbor.h_cost, neighbor))

        print("Yol bulunamadı!")
        return None
    
    def get_cost(self, x: int, y: int) -> float:
        """Calculate the cost of moving to a specific position."""
        base_cost = 1.0  # Base movement cost

        for bump in self.bumps:
            bump_grid_x = (bump.x - MAP_X) // CELL_SIZE
            bump_grid_y = (bump.y - MAP_Y) // CELL_SIZE
            if (x, y) == (bump_grid_x, bump_grid_y):  # On the bump
                base_cost *= 4.0
            elif abs(x - bump_grid_x) <= 1 and abs(y - bump_grid_y) <= 1:
                base_cost *= 2.0

        for signal in self.signals:
            signal_grid_x1 = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y1 = (signal.y - MAP_Y) // CELL_SIZE
            if (x, y) == (signal_grid_x1, signal_grid_y1) and signal.state == "red":
                base_cost *= 10.0
        
        # Yaya kontrolü
        for ped in self.pedestrians:
            if ped.current_position:
                ped_grid_x = (ped.current_position[0] - MAP_X) // CELL_SIZE
                ped_grid_y = (ped.current_position[1] - MAP_Y) // CELL_SIZE
                if abs(x - ped_grid_x) <= 1 and abs(y - ped_grid_y) <= 1:
                    if ped.state == "full" and ped.is_crossing():
                        base_cost *= 5.0  # Yaya yakınında hız beşte bire düşer
                
        return base_cost
