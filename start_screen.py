# start_screen.py
import flet as ft
from utils import make_border, ROBOT_PATH, GRID_MAX, CELL_PX, PANEL_WIDTH

def build_start_screen(page: ft.Page, show_maze_screen):
    page.clean()
    page.window.width = 700
    page.window.height = 650
    page.window.resizable = True
    page.update()

    selected = [9, 9]
    hover_pos = [9, 9]

    size_text = ft.Text(
        "N = 9 , M = 9",
        size=12, color="#00cfff",
        font_family="Consolas",
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    preview_grid = ft.Column(spacing=1)

    def build_preview():
        preview_grid.controls.clear()
        for r in range(1, GRID_MAX + 1):
            row = ft.Row(spacing=1, tight=True)
            for c in range(1, GRID_MAX + 1):
                is_selected = r <= hover_pos[0] and c <= hover_pos[1]
                is_disabled = r < 5 or c < 5

                cell = ft.Container(
                    width=CELL_PX,
                    height=CELL_PX,
                    bgcolor="#2a2a2a" if is_disabled else (
                        "#00cfff" if is_selected else "#1a1a2e"
                    ),
                    border=make_border(
                        "#3a3a3a" if is_disabled else "#7b2fff", 1
                    ),
                    border_radius=0,
                    data=(r, c),
                    on_hover=None if is_disabled else on_cell_hover,
                    on_click=None if is_disabled else on_cell_click,
                    alignment=ft.alignment.Alignment(0, 0),
                    content=ft.Text(
                        "░" if is_disabled else "",
                        size=CELL_PX - 2,
                        color="#4a4a4a",
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
                row.controls.append(cell)
            preview_grid.controls.append(row)

    def on_cell_hover(e):
        if e.data == "true":
            r, c = e.control.data
            hover_pos[0] = r
            hover_pos[1] = c
            passable_r = (r - 1) // 2
            passable_c = (c - 1) // 2
            size_text.value = f"N = {r} , M = {c}  (이동 가능 ≈ {passable_r} × {passable_c})"
            build_preview()
            preview_grid.update()
            size_text.update()

    def on_cell_click(e):
        r, c = e.control.data
        selected[0] = r
        selected[1] = c
        hover_pos[0] = r
        hover_pos[1] = c
        passable_r = (r - 1) // 2
        passable_c = (c - 1) // 2
        size_text.value = f"N = {r} , M = {c}\n(이동 가능 ≈ {passable_r} × {passable_c})  ✓"
        build_preview()
        preview_grid.update()
        size_text.update()

    build_preview()

    error_text = ft.Text("", color="#ff4444", font_family="Consolas", size=11)

    def on_start(e):
        show_maze_screen(selected[0], selected[1])

    speech_bubble = ft.Container(
        padding=ft.Padding(10, 8, 10, 8),
        bgcolor="#12122a",
        border=make_border("#00cfff", 1),
        border_radius=8,
        content=ft.Column(
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("안녕! 나는 스택봇이야 🤖", size=11,
                        color="#00cfff", font_family="Consolas",
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Text("DFS로 미로를 탐색할게!\n한 방향으로 파고들다\n막히면 되돌아와~",
                        size=10, color="#cccccc", font_family="Consolas",
                        text_align=ft.TextAlign.CENTER),
                ft.Text("스택(Stack) 자료구조 사용!", size=10,
                        color="#aaaaaa", font_family="Consolas",
                        text_align=ft.TextAlign.CENTER),
            ]
        )
    )

    center_robot = ft.Column(
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            ft.Container(height=80),
            speech_bubble,
            ft.Text("▼", size=16, color="#00cfff",
                    text_align=ft.TextAlign.CENTER),
            ft.Image(src=ROBOT_PATH, width=130, height=130),
        ]
    )

    right_panel = ft.Container(
        width=PANEL_WIDTH,
        padding=ft.Padding(12, 12, 12, 12),
        bgcolor="#12122a",
        border=make_border("#7b2fff", 1),
        border_radius=0,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
            controls=[
                ft.Text("미로 크기 선택", size=13, color="#00cfff",
                        font_family="Consolas", weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER),
                ft.Divider(height=1, color="#7b2fff"),
                ft.Text("최소 5 × 5", size=10, color="#ff8c00",
                        font_family="Consolas",
                        text_align=ft.TextAlign.CENTER),
                size_text,
                ft.Container(
                    content=preview_grid,
                    alignment=ft.alignment.Alignment(0, 0),
                ),
                error_text,
                ft.Button(
                    "▶  START",
                    on_click=on_start,
                    style=ft.ButtonStyle(
                        color="#0a0a0a",
                        bgcolor="#00cfff",
                        padding=ft.Padding(28, 10, 28, 10),
                        text_style=ft.TextStyle(
                            size=12, weight=ft.FontWeight.BOLD,
                            font_family="Consolas"
                        ),
                    ),
                ),
            ]
        )
    )

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=16,
            scroll=ft.ScrollMode.AUTO,
            controls=[
                ft.Text("DFS ALGORITHM MAZE", size=30, color="#00cfff",
                        weight=ft.FontWeight.BOLD, font_family="Consolas"),
                ft.Text("Depth First Search", size=12, color="#cccccc",
                        font_family="Consolas"),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[center_robot, right_panel],
                ),
            ]
        )
    )