import pygame
from loguru import logger
from typing import Tuple, List


class GridGame:
    def __init__(self):
        """Initialize the grid game with a rectangular clickable grid.
        Sets up the pygame window, grid dimensions, cell size and initializes game state variables."""
        pygame.init()
        self.cell_size = 60
        self.grid_size_x = 5  # Width of grid
        self.grid_size_y = 10  # Height of grid
        self.width = self.cell_size * self.grid_size_x
        self.height = self.cell_size * self.grid_size_y + 60  # Extra height for text
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Grid Counter")
        self.reset_game()
        logger.info(
            "Grid game initialized with {}x{} grid. Maximum possible moves: {}", 
            self.grid_size_x, self.grid_size_y, self.max_possible_moves
        )

    def reset_game(self):
        """Reset the game state to initial values."""
        self.grid: List[List[int]] = [
            [0 for _ in range(self.grid_size_x)] for _ in range(self.grid_size_y)
        ]
        self.counter = 1
        self.last_clicked: Tuple[int, int] | None = None
        self.game_over = False
        # Calculate maximum possible moves using Warnsdorff's algorithm
        self.max_possible_moves = self.calculate_max_moves()
        logger.info("Game reset to initial state")

    def calculate_max_moves(self) -> int:
        """Calculate maximum possible moves using Warnsdorff's algorithm.
        
        Returns:
            int: Maximum number of moves possible following knight's tour rules
        """
        def get_valid_neighbors(pos: Tuple[int, int], visited: set) -> List[Tuple[int, int]]:
            row, col = pos
            moves = [
                (row+2, col+1), (row+2, col-1), (row-2, col+1), (row-2, col-1),
                (row+1, col+2), (row+1, col-2), (row-1, col+2), (row-1, col-2)
            ]
            return [(r,c) for r,c in moves 
                    if 0 <= r < self.grid_size_y and 0 <= c < self.grid_size_x 
                    and (r,c) not in visited]
        
        def warnsdorff_tour(start_pos: Tuple[int, int]) -> int:
            visited = {start_pos}
            pos = start_pos
            
            while True:
                neighbors = get_valid_neighbors(pos, visited)
                if not neighbors:
                    break
                    
                # Choose neighbor with fewest onward moves (Warnsdorff's rule)
                next_pos = min(neighbors, 
                             key=lambda x: len(get_valid_neighbors(x, visited)))
                visited.add(next_pos)
                pos = next_pos
                
            return len(visited)

        # Try from each starting position and return maximum
        max_moves = 0
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                moves = warnsdorff_tour((i,j))
                max_moves = max(max_moves, moves)
                logger.debug(f"Starting from ({i},{j}): {moves} moves possible")
        
        return max_moves

    def get_cell_position(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        """Convert mouse position to grid coordinates.
        
        Args:
            mouse_pos: Tuple containing x,y coordinates of mouse click
            
        Returns:
            Tuple of (row, col) grid coordinates
        """
        x, y = mouse_pos
        row = y // self.cell_size
        col = x // self.cell_size
        return row, col

    def is_valid_move(self, row: int, col: int) -> bool:
        """Check if the cell is valid to click based on knight movement rules.
        
        A valid move must:
        1. Follow chess knight movement pattern (2 squares in one direction, 1 square perpendicular)
        2. Land on an empty cell (value = 0)
        3. First move can be anywhere on the grid
        
        Args:
            row: Target row position
            col: Target column position
            
        Returns:
            Boolean indicating if move is valid
        """
        if self.last_clicked is None:
            return True
        last_row, last_col = self.last_clicked
        row_diff = abs(row - last_row)
        col_diff = abs(col - last_col)
        return ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)) and self.grid[row][col] == 0

    def has_valid_moves(self) -> bool:
        """Check if there are any valid moves remaining.
        
        Scans entire grid to find empty cells that can be reached with a valid knight's move
        from the last clicked position.
        
        Returns:
            Boolean indicating if any valid moves exist
        """
        if self.last_clicked is None:
            return True
        last_row, last_col = self.last_clicked
        for i in range(self.grid_size_y):
            for j in range(self.grid_size_x):
                if self.grid[i][j] == 0:
                    row_diff = abs(i - last_row)
                    col_diff = abs(j - last_col)
                    if (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2):
                        return True
        return False

    def run(self):
        """Main game loop.
        
        Handles:
        1. Event processing (mouse clicks, quit events)
        2. Game state updates
        3. Drawing the game board
        4. Highlighting valid moves
        5. Displaying game over state
        
        Game continues until window is closed or no valid moves remain."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Reset game when R is pressed
                        self.reset_game()
                        logger.info("Game reset by user")
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    row, col = self.get_cell_position(pygame.mouse.get_pos())
                    if (
                        0 <= row < self.grid_size_y
                        and 0 <= col < self.grid_size_x
                        and self.is_valid_move(row, col)
                    ):
                        self.grid[row][col] = self.counter
                        self.counter += 1
                        self.last_clicked = (row, col)
                        logger.debug(
                            f"Cell ({row}, {col}) clicked. Counter: {self.counter}"
                        )
                        
                        if not self.has_valid_moves():
                            self.game_over = True
                            logger.info("Game over! No more valid moves available")

            # Draw grid
            self.screen.fill((255, 255, 255))
            for i in range(self.grid_size_y):
                for j in range(self.grid_size_x):
                    rect = pygame.Rect(
                        j * self.cell_size,
                        i * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    )
                    
                    if self.game_over:
                        pygame.draw.rect(self.screen, (255, 200, 200), rect)
                    else:
                        # Highlight valid knight moves in green
                        if self.last_clicked is not None:
                            last_row, last_col = self.last_clicked
                            row_diff = abs(i - last_row)
                            col_diff = abs(j - last_col)
                            if ((row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)) and self.grid[i][j] == 0:
                                pygame.draw.rect(self.screen, (200, 255, 200), rect)
                    
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

                    # Draw numbers
                    if self.grid[i][j] != 0:
                        font = pygame.font.Font(None, 36)
                        text = font.render(str(self.grid[i][j]), True, (0, 0, 0))
                        text_rect = text.get_rect(
                            center=(
                                j * self.cell_size + self.cell_size // 2,
                                i * self.cell_size + self.cell_size // 2,
                            )
                        )
                        self.screen.blit(text, text_rect)

            # Draw game over text or instructions
            font = pygame.font.Font(None, 36)
            if self.game_over:
                moves_text = f"Moves: {self.counter - 1} | Maximum possible: {self.max_possible_moves} | Press R to restart"
            else:
                moves_text = "Press R to restart game"
            text = font.render(moves_text, True, (0, 0, 0))
            text_rect = text.get_rect(
                center=(self.width // 2, self.height - 30)
            )
            self.screen.blit(text, text_rect)

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = GridGame()
    logger.info("Starting grid game")
    game.run()
