# main.py
import flet as ft
from start_screen import build_start_screen
from maze_screen import build_maze_screen

def main(page: ft.Page):
    page.title = "🧩 DFS Maze Solver"
    page.bgcolor = "#1a1a2e"
    page.padding = 20

    def show_start_screen():
        build_start_screen(page, show_maze_screen)

    def show_maze_screen(rows, cols):
        build_maze_screen(page, rows, cols, show_start_screen)

    show_start_screen()

ft.run(main)