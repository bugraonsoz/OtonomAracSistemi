from typing import List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
from grid_map import Road_x, Road_y, MAP_X, MAP_Y, CELL_SIZE

@dataclass
class Node:
    x: int  # Grid x coordinate
    y: int  # Grid y coordinate
    parent: Optional['Node'] = None

class Bfs:
    def __init__(self, road_coordinates: List[Tuple[int, int]], signals, bumps, pedestrians):
        self.road_coordinates = set(road_coordinates)
        self.signals = signals
        self.bumps = bumps
        self.pedestrians = pedestrians
        print("Bfs initialized with road coordinates:", sorted(self.road_coordinates))

    def is_valid_move(self, position: Tuple[int, int]) -> bool:
        if position not in self.road_coordinates:
            return False

        for signal in self.signals:
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if position == (signal_grid_x, signal_grid_y) and signal.state == "red":
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

    def bfs(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        if start not in self.road_coordinates or goal not in self.road_coordinates:
            print(f"Start {start} or goal {goal} is not on the road.")
            return None

        start_node = Node(start[0], start[1])
        visited = set()
        queue = deque([(start_node, [])])

        while queue:
            current, path = queue.popleft()
            current_pos = (current.x, current.y)

            if current_pos == goal:
                final_path = path + [current_pos]
                return final_path

            if current_pos not in visited:
                visited.add(current_pos)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    neighbor_x, neighbor_y = current.x + dx, current.y + dy
                    if self.is_valid_move((neighbor_x, neighbor_y)) and (neighbor_x, neighbor_y) not in visited:
                        new_path = path + [current_pos]
                        queue.append((Node(neighbor_x, neighbor_y), new_path))

        print("No path found!")
        return None

    def find_path(self, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """Wrapper method to make Bfs compatible with the interface."""
        return self.bfs(start, goal)

    def get_cost(self, x: int, y: int) -> float:
     """Calculate the cost of moving to a specific position."""
     base_cost = 1.0  # Base movement cost

     # Check for bumps
     for bump in self.bumps:
          bump_grid_x = (bump.x - MAP_X) // CELL_SIZE
          bump_grid_y = (bump.y - MAP_Y) // CELL_SIZE
          if (x, y) == (bump_grid_x, bump_grid_y):  # On the bump
               base_cost *= 4.0
          elif abs(x - bump_grid_x) <= 1 and abs(y - bump_grid_y) <= 1:
               base_cost *= 2.0

     # Check for traffic signals
     for signal in self.signals:
          signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
          signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
          if (x, y) == (signal_grid_x, signal_grid_y) and signal.state == "red":
               base_cost *= 10.0

     # Check for pedestrians
     for pedestrian in self.pedestrians:
          if pedestrian.current_position:
               ped_grid_x = (pedestrian.current_position[0] - MAP_X) // CELL_SIZE
               ped_grid_y = (pedestrian.current_position[1] - MAP_Y) // CELL_SIZE
               if abs(x - ped_grid_x) <= 1 and abs(y - ped_grid_y) <= 1:
                    if pedestrian.state == "full" and pedestrian.is_crossing():
                         base_cost *= 5.0

     return base_cost
