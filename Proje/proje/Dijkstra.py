import heapq
from typing import List, Tuple, Optional
from dataclasses import dataclass
from grid_map import Road_x, Road_y, MAP_X, MAP_Y, CELL_SIZE

@dataclass(order=True)
class Node:
    x: int = 0  # Grid x-coordinate
    y: int = 0  # Grid y-coordinate
    parent: Optional['Node'] = None  # Parent node for path reconstruction

class Dijkstra:
    def __init__(self, road_coordinates: List[Tuple[int, int]], signals, bumps, pedestrians):
        self.road_coordinates = set(road_coordinates)  # Valid road coordinates
        self.signals = signals
        self.bumps = bumps
        self.pedestrians = pedestrians
        print("Dijkstra initialized with road coordinates:", sorted(self.road_coordinates))

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

    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """Dijkstra algoritmasını kullanarak bir yol bul."""
        if start not in self.road_coordinates or end not in self.road_coordinates:
            print(f"Start {start} or end {end} is not on the road.")
            return None

        distances = {coord: float('inf') for coord in self.road_coordinates}
        previous_nodes = {coord: None for coord in self.road_coordinates}
        distances[start] = 0
        priority_queue = [(0, start)]  # (distance, node)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == end:
                break

            neighbors = self.get_neighbors(Node(x=current_node[0], y=current_node[1]))
            for neighbor in neighbors:
                neighbor_coords = (neighbor.x, neighbor.y)
                new_distance = current_distance + 1  # Assuming uniform edge cost

                if new_distance < distances[neighbor_coords]:
                    distances[neighbor_coords] = new_distance
                    previous_nodes[neighbor_coords] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor_coords))

        # Reconstruct the shortest path
        path = []
        current = end
        while current is not None:
            path.insert(0, current)
            current = previous_nodes[current]

        if path[0] == start:
            print(f"Path found: {path}")
            return path
        else:
            print("No path found!")
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
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if (x, y) == (signal_grid_x, signal_grid_y) and signal.state == "red":
                base_cost *= 10.0

        for ped in self.pedestrians:
            if ped.current_position:
                ped_grid_x = (ped.current_position[0] - MAP_X) // CELL_SIZE
                ped_grid_y = (ped.current_position[1] - MAP_Y) // CELL_SIZE
                if abs(x - ped_grid_x) <= 1 and abs(y - ped_grid_y) <= 1:
                    if ped.state == "full" and ped.is_crossing():
                        base_cost *= 5.0

        return base_cost
