import heapq
import math
from typing import List, Tuple, Set, Optional
from dataclasses import dataclass
import pygame
from grid_map import Road_x, Road_y, MAP_X, MAP_Y, CELL_SIZE


@dataclass
class Node:
    x: int  # Grid x coordinate
    y: int  # Grid y coordinate
    parent: Optional['Node'] = None
    cost: float=0.0

class PathFinder:
    def __init__(self, road_coordinates: List[Tuple[int, int]], signals, bumps, pedestrians):
        """
        Initialize the pathfinding system

        Args:
            road_coordinates: List of valid road positions
            signals: List of TrafficSignal objects
            bumps: List of Bump objects
            pedestrians: List of Pedestrian objects
        """
        self.road_coordinates = set(road_coordinates)
        self.signals = signals
        self.bumps = bumps
        self.pedestrians = pedestrians
        print("PathFinder initialized with road coordinates:", sorted(self.road_coordinates))

    def is_valid_position(self, x: int, y: int) -> bool:
        """Check if a position is valid (on road and not blocked)"""
        print(f"Checking position ({x}, {y})")

        # Önce yol üzerinde mi kontrol et
        if (x, y) not in self.road_coordinates:
            print("Position is not on road")
            return False

        # Trafik ışığı kontrolü - kırmızı ışıkta tamamen dur
        for signal in self.signals:
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if (x, y) == (signal_grid_x, signal_grid_y):
                if signal.state == "red":
                    print("Position has red traffic light - stopping")
                    return False
                else:
                    print("Position has green light - proceeding")

        # Yaya kontrolü
        for ped in self.pedestrians:
            if ped.current_position:
                ped_grid_x = (ped.current_position[0] - MAP_X) // CELL_SIZE
                ped_grid_y = (ped.current_position[1] - MAP_Y) // CELL_SIZE
                if (x, y) == (ped_grid_x, ped_grid_y) and ped.state == "full" and ped.is_crossing():
                    print("Position has crossing pedestrian")
                    return False

        print("Position is valid")
        return True

    def get_neighbors(self, node: Node) -> List[Node]:
        """Get valid neighboring positions"""
        neighbors = []
        # Tüm yönleri kontrol et (8 yön)
        directions = [
            (0, -1),  # yukarı
            (1, -1),  # sağ üst çapraz
            (1, 0),  # sağ
            (1, 1),  # sağ alt çapraz
            (0, 1),  # aşağı
            (-1, 1),  # sol alt çapraz
            (-1, 0),  # sol
            (-1, -1),  # sol üst çapraz
        ]

        print(f"\nChecking neighbors for position ({node.x}, {node.y}):")
        for dx, dy in directions:
            new_x = node.x + dx
            new_y = node.y + dy

            # Çapraz geçişlerde köşeleri kontrol et
            if abs(dx) == 1 and abs(dy) == 1:
                # Çapraz geçiş için her iki yanın da açık olması gerekir
                if not (self.is_valid_position(node.x + dx, node.y) and
                        self.is_valid_position(node.x, node.y + dy)):
                    continue

            if self.is_valid_position(new_x, new_y):
                neighbors.append(Node(new_x, new_y, parent=node))
                direction_names = ['UP', 'UP-RIGHT', 'RIGHT', 'DOWN-RIGHT',
                                   'DOWN', 'DOWN-LEFT', 'LEFT', 'UP-LEFT']
                print(
                    f"Found valid neighbor: ({new_x}, {new_y}) - Direction: {direction_names[directions.index((dx, dy))]}")

        return neighbors

    def dijkstra(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Perform Dijkstra to find the shortest path from start to end
        """
        print(f"\n=== Starting Dijkstra Search ===")
        print(f"Start: {start}")
        print(f"Goal: {end}")

        if not (self.is_valid_position(*start) and self.is_valid_position(*end)):
            print("Invalid start or goal position")
            return None

        # Başlangıç noktası
        start_node = Node(start[0], start[1], cost=0)
        visited=set()
        stack = [(start_node, [])]  # Her node ile birlikte o ana kadarki yolu da tut

        # Düğüm maliyetlerini başlat
        distances = {start_node: 0}
        previous_nodes = {start_node: None}

        # Öncelikli kuyruk
        priority_queue = [(0, start_node)]  # (mesafe, düğüm)

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            # Eğer hedef düğüme ulaşıldıysa çık
            if (current_node.x, current_node.y) == end:
                break

            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors:
                new_distance = current_distance + 1  # Burada her kenarın maliyeti 1 kabul edilir

                # Komşu düğümü daha kısa bir mesafeye güncelle
                if new_distance < distances.get(neighbor, float('inf')):
                    distances[neighbor] = new_distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (new_distance, neighbor))

        # En kısa yolu oluştur
        path = []
        current = Node(end[0], end[1])
        while current:
            path.insert(0, (current.x, current.y))
            current = previous_nodes.get(current)

        print("\n=== Path Found ===")
        print(f"Complete path: {' -> '.join(str(p) for p in path)}")
        return path

    def check_traffic_signals(self, position: Tuple[int, int]) -> bool:
        """Check if position has a red traffic signal"""
        for signal in self.signals:
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if (position[0], position[1]) == (signal_grid_x, signal_grid_y):
                if signal.state == "red":
                    print("Stopping at red light")
                    return False
                elif signal.state == "yellow":
                    print("Proceeding with caution at yellow light")
                else:
                    print("Proceeding through green light")
        return True

    def get_cost(self, x: int, y: int) -> float:
        """Get movement cost for a position"""
        base_cost = 1.0

        # Tümsek kontrolü
        for bump in self.bumps:
            bump_grid_x = (bump.x - MAP_X) // CELL_SIZE
            bump_grid_y = (bump.y - MAP_Y) // CELL_SIZE
            if (x, y) == (bump_grid_x, bump_grid_y):  # Tam tümsek üzerinde
                base_cost *= 4.0  # Tümsek üzerinde hız dörtte bire düşer
            elif abs(x - bump_grid_x) <= 1 and abs(y - bump_grid_y) <= 1:  # Tümsek yakınında
                base_cost *= 2.0  # Tümsek yakınında hız yarıya düşer

        # Trafik ışığı kontrolü - kırmızı ışığa yaklaşırken çok yavaşla
        for signal in self.signals:
            signal_grid_x = (signal.x - MAP_X) // CELL_SIZE
            signal_grid_y = (signal.y - MAP_Y) // CELL_SIZE
            if abs(x - signal_grid_x) <= 1 and abs(y - signal_grid_y) <= 1:
                if signal.state == "red":
                    base_cost *= 10.0  # Kırmızı ışık yakınında çok yavaşla
                elif signal.state == "yellow":
                    base_cost *= 3.0  # Sarı ışıkta yavaşla

        # Yaya kontrolü
        for ped in self.pedestrians:
            if ped.current_position:
                ped_grid_x = (ped.current_position[0] - MAP_X) // CELL_SIZE
                ped_grid_y = (ped.current_position[1] - MAP_Y) // CELL_SIZE
                if abs(x - ped_grid_x) <= 1 and abs(y - ped_grid_y) <= 1:
                    if ped.state == "full" and ped.is_crossing():
                        base_cost *= 5.0  # Yaya yakınında hız beşte bire düşer

        return base_cost