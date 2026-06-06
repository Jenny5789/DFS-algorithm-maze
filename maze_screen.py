# maze_screen.py
import flet as ft
from maze_logic import DFS_MazeSolver, generate_maze
from utils import make_border, CELL_SPACING, WIN_SIZE

def build_maze_screen(page: ft.Page, rows, cols, show_start_screen):
    page.clean()

    maze = generate_maze(rows, cols)
    solver = DFS_MazeSolver(maze)

    rows = len(maze)
    cols = len(maze[0])

    cell_grid = [[None for _ in range(cols)] for _ in range(rows)]

    cell_size = min(
        (WIN_SIZE - cols * CELL_SPACING) // cols,
        (WIN_SIZE - rows * CELL_SPACING) // rows,
    )
    cell_size = min(cell_size, 44)
    cell_size = max(cell_size, 12)

    grid_w = cols * cell_size + (cols - 1) * CELL_SPACING
    grid_h = rows * cell_size + (rows - 1) * CELL_SPACING

    win_w = max(grid_w + 320, 640)
    win_h = max(grid_h + 380, 640)
    page.window.width = win_w
    page.window.height = win_h
    page.window.min_width = win_w
    page.window.max_width = win_w
    page.window.min_height = win_h
    page.window.max_height = win_h
    page.window.resizable = False
    page.update()

    grid_column = ft.Column(spacing=CELL_SPACING)
    for r in range(rows):
        row = ft.Row(spacing=CELL_SPACING, tight=True)
        for c in range(cols):
            if maze[r][c] == '1':
                bg, bc = "#1a0030", "#7b2fff"
            elif maze[r][c] == 'e':
                bg, bc = "#003300", "#00ff66"
            elif maze[r][c] == 'x':
                bg, bc = "#330000", "#ff4444"
            else:
                bg, bc = "#1a1a2e", "#333355"

            cell = ft.Container(
                width=cell_size,
                height=cell_size,
                bgcolor=bg,
                border=make_border(bc),
                border_radius=0,
                alignment=ft.alignment.Alignment(0, 0),
                content=ft.Text(
                    "",
                    size=max(cell_size // 3, 7),
                    color="#0a0a0a",
                    font_family="Verdana",
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
            cell_grid[r][c] = cell
            row.controls.append(cell)
        grid_column.controls.append(row)

    maze_container = ft.Container(
        content=grid_column,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.85, "#12122a"),
        border=make_border("#7b2fff", 2),
        border_radius=0,
    )

    stack_items = ft.Column(
        spacing=2,
        scroll=ft.ScrollMode.AUTO,
        controls=[],
        height=min(grid_h, 380),
    )
    stack_size_text = ft.Text(
        "SIZE: 0",
        size=11, color="#7b2fff",
        font_family="Consolas",
        text_align=ft.TextAlign.CENTER,
    )
    stack_panel = ft.Container(
        width=170,
        padding=ft.Padding(8, 8, 8, 8),
        bgcolor="#12122a",
        border=make_border("#7b2fff", 1),
        border_radius=0,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Text("STACK", size=14, color="#00cfff",
                        font_family="Consolas", weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Divider(height=1, color="#7b2fff"),
                stack_size_text,
                ft.Text("▲ TOP", size=11, color="#7b2fff",
                        font_family="Consolas",
                        text_align=ft.TextAlign.CENTER),
                stack_items,
            ]
        )
    )

    prev_stack_set = [set()]

    def update_stack_panel(new_stack_pos):
        items = []
        for i in range(solver.stack.top, -1, -1):
            p = solver.stack.bag[i]
            if p and not solver.visited[p[0]][p[1]]:
                items.append(p)

        new_items_set = set(items)
        pushed = new_items_set - prev_stack_set[0]
        prev_stack_set[0] = new_items_set

        stack_items.controls.clear()
        stack_size_text.value = f"SIZE: {len(items)}"

        for i, p in enumerate(items[:15]):
            is_top = (i == 0)
            is_new = p in pushed
            h = 32 if is_top else max(26 - i, 18)
            bg = "#00cfff" if is_new else ("#005577" if is_top else "#003355")
            border_color = "#00ffff" if is_top else "#00cfff"
            txt_size = 13 if is_top else max(11 - i // 3, 9)
            txt_color = "#0a0a0a" if is_new else ("#ffffff" if is_top else "#aaddff")

            block = ft.Container(
                width=150,
                height=h,
                bgcolor=bg,
                border=make_border(border_color, 2 if is_top else 1),
                border_radius=0,
                content=ft.Text(
                    f"{'▶ ' if is_top else ''}({p[0]},{p[1]})",
                    size=txt_size,
                    color=txt_color,
                    font_family="Consolas",
                    weight=ft.FontWeight.BOLD if is_top else ft.FontWeight.NORMAL,
                    text_align=ft.TextAlign.CENTER,
                ),
            )
            stack_items.controls.append(block)

        if len(items) > 15:
            stack_items.controls.append(
                ft.Text(f"... +{len(items)-15}",
                        size=11, color="#555577",
                        font_family="Consolas",
                        text_align=ft.TextAlign.CENTER)
            )

        stack_size_text.update()
        stack_items.update()

    status_text = ft.Text(
        "◉  시작 대기",
        size=15, color="#00cfff",
        font_family="Consolas",
        weight=ft.FontWeight.BOLD,
    )
    step_count = ft.Text(
        "STEP: 0",
        size=13, color="#cccccc",
        font_family="Consolas",
    )
    step_num = [0]
    visit_order = [0]
    running = [True]
    processing = [False]

    btn_step = ft.Button(
        "▶  NEXT STEP",
        style=ft.ButtonStyle(
            color="#0a0a0a", bgcolor="#00cfff",
            padding=ft.Padding(20, 12, 20, 12),
            text_style=ft.TextStyle(
                size=14, weight=ft.FontWeight.BOLD,
                font_family="Consolas"
            ),
        ),
    )

    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def next_step(e):
        if not running[0] or processing[0]:
            return
        processing[0] = True

        prev_stack_pos = solver.get_stack_positions()
        pos, prev, status = solver.step()
        new_stack_pos = solver.get_stack_positions()
        new_next = solver.get_next_candidate()

        if pos is None:
            status_text.value = "◉  탐색 실패"
            page.update()
            processing[0] = False
            return

        r, c = pos
        step_num[0] += 1

        if status == "출구 도착":
            cell_grid[r][c].bgcolor = "#003355"
            cell_grid[r][c].border = make_border("#00ffff", 2)
            cell_grid[r][c].content.value = "★"
            cell_grid[r][c].content.color = "#00ffff"
            running[0] = False
            cell_grid[r][c].update()
            btn_step.text = "🏁  END"
            status_text.value = "🏁  END"
            step_count.value = f"STEP: {step_num[0]}"
            update_stack_panel(set())
            dlg = ft.AlertDialog(
                open=True,
                modal=True,   # ← 추가: 팝업 뒤 클릭 차단
                title=ft.Text("🏁  THE END", color="#00cfff",
                              font_family="Consolas",
                              weight=ft.FontWeight.BOLD),
                content=ft.Text(f"총 {step_num[0]} 스텝 만에 출구 도착!",
                                color="#cccccc", font_family="Consolas"),
                bgcolor="#12122a",
                actions=[
                    ft.TextButton("처음으로",
                        on_click=lambda e: (
                            setattr(dlg, 'open', False),
                            page.update(),
                            show_start_screen()
                        ),
                        style=ft.ButtonStyle(color="#7b2fff")),
                    ft.TextButton("다시 풀기",
                        on_click=lambda e: (
                            setattr(dlg, 'open', False),
                            page.update(),
                            build_maze_screen(page, rows, cols, show_start_screen)
                        ),
                        style=ft.ButtonStyle(color="#00cfff")),
                ],
            )
            page.overlay.append(dlg)
            page.update()
            processing[0] = False
            return


        elif status == "백트래킹":
            cell_grid[r][c].bgcolor = "#ff8c00"
            cell_grid[r][c].border = make_border("#ff8c00", 2)
            cell_grid[r][c].content.value = "✕"
            cell_grid[r][c].content.color = "#0a0a0a"
        else:
            visit_order[0] += 1
            cell_grid[r][c].bgcolor = "#00cfff"
            cell_grid[r][c].border = make_border("#00cfff", 2)
            cell_grid[r][c].content.value = str(visit_order[0])
            cell_grid[r][c].content.color = "#0a0a0a"
        cell_grid[r][c].update()

        for sr, sc in new_stack_pos:
            if not solver.visited[sr][sc]:
                cell_grid[sr][sc].bgcolor = "#1a0030"
                cell_grid[sr][sc].border = make_border("#ffdd00")
                cell_grid[sr][sc].update()

        for sr, sc in prev_stack_pos:
            if (sr, sc) not in new_stack_pos and not solver.visited[sr][sc]:
                cell_grid[sr][sc].bgcolor = "#1a1a2e"
                cell_grid[sr][sc].border = make_border("#333355")
                cell_grid[sr][sc].update()

        if new_next and not solver.visited[new_next[0]][new_next[1]]:
            nr2, nc2 = new_next
            cell_grid[nr2][nc2].bgcolor = "#1a0030"
            cell_grid[nr2][nc2].border = make_border("#ffffff", 2)
            cell_grid[nr2][nc2].update()

        update_stack_panel(new_stack_pos)
        status_text.value = f"◉  ({r}, {c})"
        step_count.value = f"STEP: {step_num[0]}"
        page.update()
        processing[0] = False

    btn_step.on_click = next_step

    def go_back(e):
        page.window.resizable = True
        show_start_screen()

    btn_back = ft.TextButton(
        "← 처음으로",
        on_click=go_back,
        style=ft.ButtonStyle(color="#aaaaaa"),
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("DFS ALGORITHM MAZE", size=22,
                                color="#00cfff",
                                weight=ft.FontWeight.BOLD,
                                font_family="Consolas"),
                        btn_back,
                    ]
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=12,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[maze_container, stack_panel],
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[status_text, step_count],
                ),
                btn_step,
                ft.Container(height=10),
            ]
        )
    )