"""
Fake implementations of GoBase.

We provide a GoStub implementation, and you must
implement a GoFake implementation.
"""
from copy import deepcopy

from base import GoBase, BoardGridType, ListMovesType


class GoStub(GoBase):
    """
    Stub implementation of GoBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.

    - The board is always initialized with four pieces in the four
      corners of the board. Player 1 has pieces in the northeast and
      southwest corners of the board, and Player 2 has pieces in the
      southeast and northwest corners of the board.
    - Players are allowed to place pieces in any position of the board
      they want, even if there is already a piece in that position
      (placing a piece in such a position replaces the previous piece
      with the new one). The ko and superko rule do not apply.
    - The game ends after four moves. Whatever player has a piece in
      position (0,1) wins. If there is no piece in that position,
      the game ends in a tie.
    - The scores are always reported as 100 for Player 1 and 200 for
      Player 2. Note how the scores do not play a role in determining
      the outcome of the game.
    - It does not validate board positions. If a method is called with
      a position outside the board, the method will likely cause an exception.
    - It does not implement the load_game or simulate_moves method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, superko: bool = False):
        """
        See GoBase.__init__
        """
        if players != 2:
            raise ValueError(
                "The stub implementation " "only supports two players"
            )

        super().__init__(side, players, superko)

        self._grid = [[None] * side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        """
        See GoBase.grid
        """
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        """
        See GoBase.turn
        """
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        """
        See GoBase.available_moves
        """
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        """
        See GoBase.done
        """
        return self._num_moves == 4

    @property
    def outcome(self) -> list[int]:
        """
        See GoBase.outcome
        """
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [1, 2]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: tuple[int, int]) -> int | None:
        """
        See GoBase.piece_at
        """
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: tuple[int, int]) -> bool:
        """
        See GoBase.legal_move
        """
        return True

    def apply_move(self, pos: tuple[int, int]) -> None:
        """
        See GoBase.apply_move
        """
        r, c = pos
        self._grid[r][c] = self._turn
        self.pass_turn()

    def pass_turn(self) -> None:
        """
        See GoBase.pass_turn
        """
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def scores(self) -> dict[int, int]:
        """
        See GoBase.scores
        """
        return {1: 100, 2: 200}

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        See GoBase.load_game
        """
        raise NotImplementedError

    def simulate_move(self, pos: tuple[int, int] | None) -> "GoBase":
        """
        See GoBase.simulate_move
        """
        raise NotImplementedError


#
# Your GoFake implementation goes here
#

