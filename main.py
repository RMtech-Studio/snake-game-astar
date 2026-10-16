"""
=============================================================================
SNAKE GAME AI - THUẬT TOÁN TÌM ĐƯỜNG A* (A-STAR SEARCH)
KÊNH: RMtech • Code Game Thực Chiến & Kiểm Chứng Thuật Toán
MÃ NGUỒN TẬP 02: https://github.com/RMtech-Studio/snake-game-astar
=============================================================================
"""

import sys
import random
import heapq
from collections import deque
import pygame

# 1. CẤU HÌNH BÀN CỜ & ĐỒ HỌA
GRID_COLS, GRID_ROWS = 24, 16
CELL_SIZE = 36
WIDTH = GRID_COLS * CELL_SIZE
HEIGHT = GRID_ROWS * CELL_SIZE
FPS = 15  # Tốc độ di chuyển của Rắn (15 bước/giây)

# Bảng màu Công nghệ Neon (RMtech Dark Theme)
COLOR_BG = (15, 23, 42)          # Nền xanh đen Slate 900
COLOR_GRID = (30, 41, 59)        # Lưới Slate 800
COLOR_SNAKE_HEAD = (56, 189, 248)# Đầu rắn Cyan sáng
COLOR_SNAKE_BODY = (14, 165, 233)# Thân rắn Blue
COLOR_FOOD = (239, 68, 68)       # Quả táo Red Neon
COLOR_PATH = (245, 158, 11)      # Đường đi A* Vàng Hổ Phách (Amber)
COLOR_VISITED = (30, 58, 80)     # Các ô A* đã duyệt thử qua (Mờ)
COLOR_TEXT = (248, 250, 252)     # Chữ trắng


# 2. HÀM HEURISTIC KHOẢNG CÁCH MANHATTAN (TAXICAB GEOMETRY)
def heuristic(a, b):
    """
    Khoảng cách Manhattan: h(n) = |x1 - x2| + |y1 - y2|
    Phù hợp hoàn hảo cho lưới 4 hướng (không đi chéo).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# 3. THUẬT TOÁN TÌM ĐƯỜNG A* (A-STAR SEARCH)
def get_astar_path(head, target, body_set):
    """
    Thuật toán tìm đường A* sử dụng Priority Queue (heapq).
    Mỗi node lưu (f_score, g_score, current_pos, path).
    - g(n): Chi phí thực tế đã đi từ đầu đến node hiện tại.
    - h(n): Ước lượng khoảng cách Manhattan từ node tới quả táo.
    - f(n) = g(n) + h(n): Ước lượng tổng chi phí.
    """
    # open_set lưu: (f_score, g_score, count, curr_pos, path)
    count = 0
    open_heap = []
    initial_h = heuristic(head, target)
    heapq.heappush(open_heap, (initial_h, 0, count, head, []))
    
    # g_scores lưu chi phí thấp nhất đến từng ô
    g_scores = {head: 0}
    visited_cells = set()

    while open_heap:
        f, g, _, curr, path = heapq.heappop(open_heap)
        visited_cells.add(curr)

        # Khi chạm đích (quả táo)
        if curr == target:
            return path, visited_cells

        # Duyệt 4 hướng lân cận: Phải, Xuống, Trái, Lên
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = curr[0] + dx, curr[1] + dy
            neighbor = (nx, ny)

            # Kiểm tra trong biên và không đâm vào thân rắn
            if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS:
                if neighbor not in body_set:
                    tentative_g = g + 1
                    if tentative_g < g_scores.get(neighbor, float('inf')):
                        g_scores[neighbor] = tentative_g
                        h = heuristic(neighbor, target)
                        f_score = tentative_g + h
                        count += 1
                        heapq.heappush(open_heap, (f_score, tentative_g, count, neighbor, path + [(dx, dy)]))

    # Không tìm thấy đường tới mồi (bị thân bao vây)
    return [], visited_cells


# 4. CHƯƠNG TRÌNH CHÍNH PYGAME
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT + 60))
    pygame.display.set_caption("RMtech • Snake Game AI: Thuật Toán Tìm Đường A*")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Consolas", 20, bold=True)

    # Khởi tạo Rắn: 3 đốt ban đầu ở giữa bàn cờ
    snake = deque([(8, 8), (7, 8), (6, 8)])
    score = 0
    nodes_evaluated = 0

    # Sinh quả táo ngẫu nhiên không trùng thân rắn
    def spawn_food():
        while True:
            f = (random.randint(0, GRID_COLS - 1), random.randint(0, GRID_ROWS - 1))
            if f not in snake:
                return f

    food = (18, 8)
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- BƯỚC TÍNH TOÁN CỦA AI A* ---
        head = snake[0]
        # Tập hợp thân rắn (trừ đuôi cuối vì đuôi sẽ di chuyển theo)
        body_set = set(list(snake)[:-1])
        
        path, visited_nodes = get_astar_path(head, food, body_set)
        nodes_evaluated = len(visited_nodes)

        if path:
            move = path[0]
        else:
            # Dự phòng khi bị kẹt: Đi ô hợp lệ bất kỳ
            move = None
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = head[0] + dx, head[1] + dy
                if 0 <= nx < GRID_COLS and 0 <= ny < GRID_ROWS and (nx, ny) not in body_set:
                    move = (dx, dy)
                    break
            if move is None:
                move = (1, 0)  # Chấp nhận va chạm kết thúc ván

        new_head = (head[0] + move[0], head[1] + move[1])

        # Kiểm tra tự đâm vào thân hoặc đâm tường
        if new_head in body_set or not (0 <= new_head[0] < GRID_COLS and 0 <= new_head[1] < GRID_ROWS):
            print(f"Game Over! Điểm số đạt được: {score}")
            snake = deque([(8, 8), (7, 8), (6, 8)])
            score = 0
            food = spawn_food()
            continue

        snake.appendleft(new_head)

        # Kiểm tra ăn mồi
        if new_head == food:
            score += 10
            food = spawn_food()
        else:
            snake.pop()

        # --- VẼ GIAO DIỆN LÊN MÀN HÌNH ---
        screen.fill(COLOR_BG)

        # 1. Vẽ lưới bàn cờ
        for c in range(GRID_COLS):
            for r in range(GRID_ROWS):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, COLOR_GRID, rect, 1)

        # 2. Vẽ các ô A* đã duyệt thử (Visited Nodes)
        for vx, vy in visited_nodes:
            v_rect = pygame.Rect(vx * CELL_SIZE + 4, vy * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
            pygame.draw.rect(screen, COLOR_VISITED, v_rect, border_radius=4)

        # 3. Vẽ vệt đường đi tối ưu A* (Vàng Hổ Phách)
        curr_p = head
        for step in path:
            next_p = (curr_p[0] + step[0], curr_p[1] + step[1])
            px = next_p[0] * CELL_SIZE + CELL_SIZE // 2
            py = next_p[1] * CELL_SIZE + CELL_SIZE // 2
            pygame.draw.circle(screen, COLOR_PATH, (px, py), 5)
            curr_p = next_p

        # 4. Vẽ Quả Táo (Đỏ Neon)
        fx, fy = food[0] * CELL_SIZE, food[1] * CELL_SIZE
        pygame.draw.rect(screen, COLOR_FOOD, (fx + 4, fy + 4, CELL_SIZE - 8, CELL_SIZE - 8), border_radius=8)

        # 5. Vẽ Thân & Đầu Rắn
        for i, (sx, sy) in enumerate(snake):
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            s_rect = pygame.Rect(sx * CELL_SIZE + 2, sy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(screen, color, s_rect, border_radius=6)
            if i == 0:
                # Vẽ mắt rắn
                pygame.draw.circle(screen, (15, 23, 42), (sx * CELL_SIZE + CELL_SIZE // 2, sy * CELL_SIZE + CELL_SIZE // 2), 3)

        # 6. Thanh Bảng Điều Khiển Telemetry Dưới Đáy
        hud_rect = pygame.Rect(0, HEIGHT, WIDTH, 60)
        pygame.draw.rect(screen, (24, 32, 47), hud_rect)
        pygame.draw.line(screen, (51, 65, 85), (0, HEIGHT), (WIDTH, HEIGHT), 2)

        txt_score = font.render(f"SCORE: {score:03d}", True, (52, 211, 153))
        txt_algo = font.render("ALGORITHM: A* HEURISTIC", True, (245, 158, 11))
        txt_eval = font.render(f"NODES EVALUATED: {nodes_evaluated:02d} (BFS: ~65)", True, (56, 189, 248))
        
        screen.blit(txt_score, (20, HEIGHT + 18))
        screen.blit(txt_algo, (220, HEIGHT + 18))
        screen.blit(txt_eval, (550, HEIGHT + 18))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
