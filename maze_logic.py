# maze_logic.py
import random

PASSABLE = {'0', 'e', 'x'}
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def generate_maze(rows, cols):
    # 최소 크기 및 홀수 보정
    rows = max(rows, 5)
    cols = max(cols, 5)
    if rows % 2 == 0: rows += 1
    if cols % 2 == 0: cols += 1

    maze = [['1'] * cols for _ in range(rows)]

    def carve(r, c):
        maze[r][c] = '0'
        dirs = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(dirs)
        for dr, dc in dirs:
            nr, nc = r + dr, c + dc
            if 0 < nr < rows and 0 < nc < cols and maze[nr][nc] == '1':
                maze[r + dr//2][c + dc//2] = '0'
                carve(nr, nc)

    carve(1, 1)

    loop_count = (rows * cols) // 8
    attempts = 0
    added = 0
    while added < loop_count and attempts < loop_count * 10:
        attempts += 1
        r = random.randrange(1, rows - 1)
        c = random.randrange(1, cols - 1)
        if maze[r][c] != '1':
            continue
        if maze[r-1][c] == '0' and maze[r+1][c] == '0':
            maze[r][c] = '0'
            added += 1
        elif maze[r][c-1] == '0' and maze[r][c+1] == '0':
            maze[r][c] = '0'
            added += 1

    maze[1][1] = 'e'
    maze[rows - 2][cols - 2] = 'x'
    return maze

def find_pos(maze, target):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == target:
                return (r, c)
    return None

class ADT_stack:
    def __init__(self, capacity=1000):
        self.maxsize = capacity
        self.bag = [None] * self.maxsize
        self.top = -1

    def push(self, e):
        if self.top < self.maxsize - 1:
            self.top += 1
            self.bag[self.top] = e
            return True
        return False

    def pop(self):
        if self.top != -1:
            popped = self.bag[self.top]
            self.bag[self.top] = None
            self.top -= 1
            return popped
        return None

    def isEmpty(self):
        return self.top == -1

class DFS_MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.stack = ADT_stack(self.rows * self.cols * 4)
        self.visited = [[False] * self.cols for _ in range(self.rows)]
        self.in_stack = [[False] * self.cols for _ in range(self.rows)]
        self.start_pos = find_pos(maze, 'e')
        self.exit_pos = find_pos(maze, 'x')
        self.prev_pos = None
        self.stack.push(self.start_pos)
        self.in_stack[self.start_pos[0]][self.start_pos[1]] = True

    def step(self):
        if self.stack.isEmpty():
            return None, None, "탐색 실패"
        current = self.stack.pop()
        r, c = current
        self.in_stack[r][c] = False
        if self.visited[r][c]:
            return self.step()
        self.visited[r][c] = True


        prev = self.prev_pos 

        if current == self.exit_pos:
            return current, self.prev_pos, "출구 도착"
        pushed_any = False
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.maze[nr][nc] in PASSABLE and not self.visited[nr][nc]:
                    self.stack.push((nr, nc))
                    self.in_stack[nr][nc] = True
                    pushed_any = True
        status = "탐색 중" if pushed_any else "백트래킹"
        self.prev_pos = current 
        return current, prev, status  
        return current, self.prev_pos, status

    def get_stack_positions(self):
        positions = set()
        for i in range(self.stack.top + 1):
            if self.stack.bag[i] is not None:
                positions.add(self.stack.bag[i])
        return positions

    def get_next_candidate(self):
        for i in range(self.stack.top, -1, -1):
            pos = self.stack.bag[i]
            if pos and not self.visited[pos[0]][pos[1]]:
                return pos
        return None