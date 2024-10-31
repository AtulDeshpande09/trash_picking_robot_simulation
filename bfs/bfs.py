from collections import deque
#from main import load_map

# Define BFS function
def bfs(grid, start, goal, accessible_tiles=['.', 'T', 'G', 'D']):
    # Initialize queue and visited set
    queue = deque([start])  # Start with the bot’s start position
    visited = set([start])  # Keep track of visited tiles
    parents = {}  # To reconstruct path later

    # Define directions for up, down, left, and right movement
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    while queue:
        # Get the current tile to explore
        current = queue.popleft()
        x, y = current
        
        # If we've reached the goal, reconstruct the path
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = parents[current]
            path.reverse()  # Reverse the path to go from start to goal
            return path  # Return the path as a list of tiles
        
        # Explore neighbors
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)

            # Check if neighbor is within bounds and accessible
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and neighbor not in visited:
                if grid[ny][nx] in accessible_tiles:
                    queue.append(neighbor)
                    visited.add(neighbor)
                    parents[neighbor] = current  # Track the parent for path reconstruction
    
    # If no path was found
    return None


if __name__ == '__main__':
    grid2 = load_map("c_map2.txt")
    start_position = (0, 0)
    goal_position = (11,11)
    path = bfs(grid2, start_position, goal_position)
    print(f"Path found by BFS: {path}")