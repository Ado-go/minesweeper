import tkinter as tk
from random import choice

Width = 500
Height = 500

Number_of_bombs = 50
Tile_size = 15
Rows = 20
Cols = 20

root = tk.Tk()
root.title("Minesweeper")
canvas = tk.Canvas(width=Width, height=Height)
canvas.pack()


class Game:
    def __init__(self, rows, cols, tile_size, number_of_bombs):
        self.x = 0
        self.y = 0
        self.tile_size = tile_size
        self.number_of_tiles = rows * cols
        self.number_of_bombs = number_of_bombs
        self.number_of_flags = 0
        self.flags = []
        self.field = []
        self.rows = cols
        self.cols = rows
        self.game_over = False

        self.create_plan()
        self.plant_bombs()
        self.add_numbers_near_bombs()
        self.draw_field()

    def game_restart(self, _):
        self.x = 0
        self.y = 0
        self.tile_size = self.tile_size
        self.number_of_tiles = self.rows * self.cols
        self.number_of_bombs = self.number_of_bombs
        self.number_of_flags = 0
        self.flags = []
        self.field = []
        self.rows = self.rows
        self.cols = self.cols
        self.game_over = False

        self.create_plan()
        self.plant_bombs()
        self.add_numbers_near_bombs()
        self.draw_field()

    def create_plan(self):
        for i in range(self.rows):
            self.field.append([])
            for j in range(self.cols):
                self.field[i].append(0)

    def plant_bombs(self):
        free_rows = [i for i in range(self.rows)]
        for bomb in range(self.number_of_bombs):
            selected_row = choice(free_rows)
            free_cols = [j for j in range(self.cols) if self.field[selected_row][j] == 0]
            if len(free_cols) == 1:
                free_rows.remove(selected_row)
            selected_col = choice(free_cols)
            self.field[selected_row][selected_col] = "mine"

    def add_numbers_near_bombs(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] != "mine":
                    adjacent = []
                    if i > 0:
                        adjacent.append(self.field[i-1][j])
                    if i < self.rows - 1:
                        adjacent.append(self.field[i+1][j])
                    if j > 0:
                        adjacent.append(self.field[i][j-1])
                    if j < self.cols - 1:
                        adjacent.append(self.field[i][j+1])
                    if j > 0 and i > 0:
                        adjacent.append(self.field[i-1][j-1])
                    if j < self.cols - 1 and i < self.rows - 1:
                        adjacent.append(self.field[i+1][j+1])
                    if j < self.cols - 1 and i > 0:
                        adjacent.append(self.field[i-1][j+1])
                    if j > 0 and i < self.rows - 1:
                        adjacent.append(self.field[i+1][j-1])
                    for tile in adjacent:
                        if tile == "mine":
                            self.field[i][j] += 1

    def draw_field(self):
        canvas.delete("all")
        col_space = self.y
        for row in range(self.rows):
            row_space = self.x
            for col in range(self.cols):
                if self.field[row][col] == "mine":
                    canvas.create_rectangle(row_space, col_space,
                                            row_space + self.tile_size, col_space + self.tile_size, fill="red")
                    tile = canvas.create_rectangle(row_space, col_space,
                                                   row_space + self.tile_size,
                                                   col_space + self.tile_size, fill="#a3a3a3")
                    self.field[row][col] = Tile(row, col, "mine", tile)
                elif self.field[row][col] == 0:
                    canvas.create_rectangle(row_space, col_space, row_space
                                            + self.tile_size, col_space + self.tile_size, fill="light grey")
                    tile = canvas.create_rectangle(row_space, col_space, row_space + self.tile_size,
                                                   col_space + self.tile_size, fill="#a3a3a3")
                    self.field[row][col] = Tile(row, col, "empty", tile)
                else:
                    canvas.create_rectangle(row_space, col_space,
                                            row_space + self.tile_size, col_space + self.tile_size, fill="light grey")
                    colors = ["blue", "green", "red", "dark blue", "brown", "dark cyan", "black", "grey"]
                    canvas.create_text(row_space + self.tile_size//2,
                                       col_space + self.tile_size//2,
                                       text=self.field[row][col],
                                       font=("Arial", (self.tile_size // 3) * 2), fill=colors[self.field[row][col]-1])
                    tile = canvas.create_rectangle(row_space, col_space, row_space + self.tile_size,
                                                   col_space + self.tile_size, fill="#a3a3a3")
                    self.field[row][col] = Tile(row, col, "number", tile)
                row_space += self.tile_size
            col_space += self.tile_size

    def clicked_on_tile(self, tile):
        tile.deleted = True
        if tile.under == "mine":
            self.game_over = True
            for row in self.field:
                for tiles in row:
                    canvas.delete(tiles.canvas_id)
            canvas.create_text(Width // 2, Height - 60, text="Game over", font=("Arial", 40))

        elif tile.under == "empty":
            self.chain_reaction(tile)
        else:
            canvas.delete(tile.canvas_id)
            self.number_of_tiles -= 1

    def add_flag(self, tile):
        if not tile.deleted:
            tile.flagged = not tile.flagged
        if tile.flagged:
            self.number_of_flags += 1
            flag_size = self.tile_size // 4
            flag = canvas.create_rectangle(self.tile_size * tile.col + self.x * tile.col + self.tile_size // 2 - flag_size,
                                           self.tile_size * tile.row + self.y * tile.row + self.tile_size // 2 - flag_size,
                                           self.tile_size * tile.col + self.x * tile.col + flag_size + self.tile_size // 2,
                                           self.tile_size * tile.row + self.y * tile.row + flag_size + self.tile_size // 2,
                                           fill="green")
            tile.flag_id = flag
        else:
            self.number_of_flags -= 1
            canvas.delete(tile.flag_id)
            tile.flag_id = None

    def chain_reaction(self, tile):
        tile.deleted = True
        canvas.delete(tile.canvas_id)
        self.number_of_tiles -= 1
        adjacent = []
        if tile.row > 0:
            adjacent.append(self.field[tile.row - 1][tile.col])
        if tile.row < self.rows - 1:
            adjacent.append(self.field[tile.row + 1][tile.col])
        if tile.col > 0:
            adjacent.append(self.field[tile.row][tile.col - 1])
        if tile.col < self.cols - 1:
            adjacent.append(self.field[tile.row][tile.col + 1])
        if tile.row > 0 and tile.col > 0:
            adjacent.append(self.field[tile.row - 1][tile.col - 1])
        if tile.row < self.rows - 1 and tile.col < self.cols - 1:
            adjacent.append(self.field[tile.row + 1][tile.col + 1])
        if tile.row > 0 and tile.col < self.cols - 1:
            adjacent.append(self.field[tile.row - 1][tile.col + 1])
        if tile.row < self.rows - 1 and tile.col > 0:
            adjacent.append(self.field[tile.row + 1][tile.col - 1])
        for tile in adjacent:
            if tile.under == "empty" and not tile.deleted and not tile.flagged:
                self.chain_reaction(tile)
            elif not tile.deleted and not tile.flagged:
                tile.deleted = True
                canvas.delete(tile.canvas_id)
                self.number_of_tiles -= 1


class Tile:
    def __init__(self, row, col, under, canvas_id):
        self.row = row
        self.col = col
        self.under = under
        self.canvas_id = canvas_id
        self.deleted = False
        self.flagged = False
        self.flag_id = None

    def add_flag_id(self, flag_id):
        self.flag_id = flag_id


def click(event):
    if not game.game_over:
        col = ((event.x - game.x) // game.tile_size)
        row = ((event.y - game.y) // game.tile_size)
        if game.cols - 1 >= col >= 0 and game.rows - 1 >= row >= 0:
            if not game.field[row][col].deleted:
                if event.num == 1 and not game.field[row][col].flagged:
                    game.clicked_on_tile(game.field[row][col])
                elif event.num == 3:
                    game.add_flag(game.field[row][col])
    if game.number_of_flags == game.number_of_bombs == game.number_of_tiles and not game.game_over:
        game.game_over = True
        canvas.create_text(Width//2, Height - 60, text="Victory", font=("Arial", 40))


game = Game(Rows, Cols, Tile_size, Number_of_bombs)


canvas.bind("<ButtonRelease-1>", click)
canvas.bind("<ButtonRelease-3>", click)
canvas.bind_all("r", game.game_restart)
canvas.mainloop()
