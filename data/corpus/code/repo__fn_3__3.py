def nextGen(self):
        
        self.current_gen += 1
        self.change_gen[self.current_gen % 3] = copy.copy(self.grid)
        grid_cp = copy.copy(self.grid)

        for cell in self.grid:
            y, x = cell
            y1 = (y - 1) % self.y_grid
            y2 = (y + 1) % self.y_grid
            x1 = (x - 1) % self.x_grid
            x2 = (x + 1) % self.x_grid
            n = self.countNeighbours(cell)

            if n < 2 or n > 3:
                del grid_cp[cell]
                self.addchar(y + self.y_pad, x + self.x_pad, ' ')
            else:
                grid_cp[cell] = min(self.grid[cell] + 1, self.color_max)

            for neighbour in product([y1, y, y2], [x1, x, x2]):
                if not self.grid.get(neighbour):
                    if self.countNeighbours(neighbour) == 3:
                        y, x = neighbour
                        y = y % self.y_grid
                        x = x % self.x_grid
                        neighbour = y, x
                        grid_cp[neighbour] = 1

        self.grid = grid_cp