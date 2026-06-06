# utils.py
import os
import flet as ft

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROBOT_PATH = os.path.join(BASE_DIR, "robot.png")

CELL_SPACING = 2
GRID_MAX = 15
CELL_PX = 10
WIN_SIZE = 480
PANEL_HEIGHT = 340
PANEL_WIDTH = 260

def make_border(color, width=1):
    return ft.Border(
        top=ft.BorderSide(width, color),
        bottom=ft.BorderSide(width, color),
        left=ft.BorderSide(width, color),
        right=ft.BorderSide(width, color),
    )

