"""
Game Logic Organism - org_game_logic_gen0_e828cd
Archetype: game_logic
Generation: 0
Fitness: 0.433
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CellState(Enum):
    EMPTY = " "
    X = "X"
    O = "O"


@dataclass
class GameBoard:
    """Simple game board"""
    size: int = 3
    cells: List[List[CellState]] = None
    
    def __post_init__(self):
        if self.cells is None:
            self.cells = [
                [CellState.EMPTY] * self.size 
                for _ in range(self.size)
            ]
    
    def place(self, row: int, col: int, state: CellState) -> bool:
        """Place piece on board"""
        if 0 <= row < self.size and 0 <= col < self.size:
            if self.cells[row][col] == CellState.EMPTY:
                self.cells[row][col] = state
                return True
        return False
    
    def check_winner(self) -> Optional[CellState]:
        """Check for winner"""
        # Check rows
        for row in self.cells:
            if row[0] != CellState.EMPTY and all(c == row[0] for c in row):
                return row[0]
        
        # Check columns
        for col in range(self.size):
            if self.cells[0][col] != CellState.EMPTY:
                if all(self.cells[row][col] == self.cells[0][col] 
                       for row in range(self.size)):
                    return self.cells[0][col]
        
        return None
    
    def __str__(self) -> str:
        lines = []
        for row in self.cells:
            lines.append("|" + "|".join(c.value for c in row) + "|")
        return "\n".join(lines)


def run_organism():
    """Organism entry point"""
    board = GameBoard()
    board.place(0, 0, CellState.X)
    board.place(1, 1, CellState.X)
    board.place(2, 2, CellState.X)
    winner = board.check_winner()
    print(f"Board:\n{board}")
    print(f"Winner: {winner}")
    return board


if __name__ == "__main__":
    run_organism()
