import pytest

from base import GoBase
from fakes import GoFake


def test_inheritance() -> None:
    """Test that GoFake inherits from GoBase"""
    assert issubclass(GoFake, GoBase), "GoFake should inherit from GoBase"


def test_init() -> None:
    """Test that a GoFake object is constructed correctly"""
    GoFake(19, 2)


def test_init_properties() -> None:
    """Test the properties of a GoFake object after it is constructed"""
    go = GoFake(19, 2)

    assert go.size == 19
    assert go.num_players == 2
    assert go.turn == 1
    assert not go.done
    assert go.outcome == []


def test_init_legal_move() -> None:
    """
    Test that we can make a move in any location of a
    newly created game
    """

    go = GoFake(19, 2)

    for row in range(19):
        for col in range(19):
            assert go.legal_move((row, col))


@pytest.mark.parametrize(
    "row,col",
    [
        (-1, -1),
        (-1, 5),
        (-1, 19),
        (5, -1),
        (5, 19),
        (19, -1),
        (19, 5),
        (19, 19),
    ],
)
def test_legal_move_invalid_location(row: int, col: int) -> None:
    """
    Test that checking for a legal move outside the board raises an exception
    """
    go = GoFake(19, 2)

    with pytest.raises(ValueError):
        go.legal_move((row, col))


def test_basic_moves_1() -> None:
    """Check that we can place a piece successfully"""

    go = GoFake(19, 2)
    pos = (5, 5)

    assert go.legal_move(pos)

    go.apply_move(pos)

    assert go.piece_at(pos) == 1


def test_basic_moves_2() -> None:
    """
    Check that we can place multiple pieces successfully
    (and that the turn updates between each move)
    """

    go = GoFake(19, 2)

    pos = (5, 5)
    assert go.legal_move(pos)
    go.apply_move(pos)
    assert go.piece_at(pos) == 1

    pos = (18, 18)
    assert go.legal_move(pos)
    go.apply_move(pos)
    assert go.piece_at(pos) == 2

    pos = (0, 0)
    assert go.legal_move(pos)
    go.apply_move(pos)
    assert go.piece_at(pos) == 1


def test_basic_moves_3() -> None:
    """Check that we can't place a piece in an occupied location"""

    go = GoFake(19, 2)

    pos = (5, 5)
    assert go.legal_move(pos)
    go.apply_move(pos)

    assert not go.legal_move(pos)


def test_grid_1() -> None:
    """Check that grid for an empty game is exported correctly"""

    go = GoFake(19, 2)

    grid = go.grid

    for row in range(go.size):
        for col in range(go.size):
            assert grid[row][col] is None


def test_grid_2() -> None:
    """
    Check that grid returns a deep copy of the board's grid,
    and that modifying grid's return value doesn't modify
    the game's board
    """

    go = GoFake(19, 2)

    grid = go.grid

    grid[5][5] = 1

    assert go.piece_at((5, 5)) is None, (
        "grid() returned a shallow copy of the game's board. "
        "Modifying the return value of grid() should not "
        "affect the game's board."
    )


def test_grid_3() -> None:
    """
    Check that grid returns a correct copy of the board after making
    a few moves (none of the moves will result in a capture)
    """

    moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (12, 2),
    ]

    go = GoFake(19, 2)

    for move in moves:
        go.apply_move(move)

    grid = go.grid

    for row in range(go.size):
        for col in range(go.size):
            assert grid[row][col] == go.piece_at((row, col))


def test_capture_1() -> None:
    """
    Check that we capture a piece. We place one piece in
    position (5, 6) and then place a piece in position (5, 7).
    The piece in position (5, 6) should be captured.
    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    go.apply_move((5, 7))
    assert go.piece_at((5, 7)) == 2
    assert go.piece_at((5, 6)) is None


def test_capture_2() -> None:
    """
    Check that we can capture in all directions

    We will set up the following:

          5  6  7
       4  ·  B  ·
       5  B  .  B
       6  ·  B  ·

    (plus three white pieces in other positions of the board
    that have no effect on the outcome of the test.)

    Making a white move in 5,6 should result in
    all four black pieces being captured.
    """
    moves = [(5, 5), (9, 0), (5, 7), (9, 1), (4, 6), (9, 2), (6, 6)]

    go = GoFake(19, 2)

    for move in moves:
        go.apply_move(move)

    for pos in [(5, 5), (5, 7), (4, 6), (6, 6)]:
        assert go.piece_at(pos) == 1

    go.apply_move((5, 6))

    assert go.piece_at((5, 6)) == 2
    for pos in [(5, 5), (5, 7), (4, 6), (6, 6)]:
        assert go.piece_at(pos) is None


def test_capture_3() -> None:
    """
    Check that we do not capture pieces in diagonal directions

    We will set up the following:

          5  6  7
       4  B  .  B
       5  .  .  .
       6  B  .  B

    (plus three white pieces in other positions of the board
    that have no effect on the outcome of the test.)

    Making a white move in 5,6 should result in
    all four black pieces being captured.
    """
    moves = [(4, 5), (9, 0), (4, 7), (9, 1), (6, 5), (9, 2), (6, 7)]

    go = GoFake(19, 2)

    for move in moves:
        go.apply_move(move)

    for pos in [(4, 5), (4, 7), (6, 5), (6, 7)]:
        assert go.piece_at(pos) == 1

    go.apply_move((5, 6))

    assert go.piece_at((5, 6)) == 2
    for pos in [(4, 5), (4, 7), (6, 5), (6, 7)]:
        assert go.piece_at(pos) == 1


def test_ko_1() -> None:
    """
    Check that the ko rule is enforced

    Like test_capture_1, we place a black piece in
    position (5, 6) and then place a white piece in position (5, 7).
    The black piece in position (5, 6) should be captured.
    Placing a black piece in position (5, 6) would capture the
    piece in position (5, 7), which would violate the ko rule
    (because we've gone back to the previous state, where we
    has a single black piece in (5, 6))

    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    go.apply_move((5, 7))
    assert go.piece_at((5, 7)) == 2
    assert go.piece_at((5, 6)) is None

    assert not go.legal_move((5, 6)), (
        "Placing a black piece in (5, 6) violates the ko rule, "
        "but legal_move() returned True"
    )


def test_ko_2() -> None:
    """
    Check that the ko rule is only enforced for the immediately
    prior state. We place the following pieces

    - BLACK @ (5, 6)
    - WHITE @ (5, 7) [Captures black piece at (5, 6)]
    - BLACK @ (6, 7) [Captures white piece at (5, 7)]
    - WHITE @ (6, 6) [Captures black piece at (6, 7)]
    - BLACK @ (5, 6) [Captures white piece at (6, 6)]

    At the end, there should be a single black piece in (5, 6).
    This is the same state as after the first move, but not a violation
    of the Ko rule, because it does not return the board to an immediately
    previous state.
    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    go.apply_move((5, 7))
    assert go.piece_at((5, 7)) == 2
    assert go.piece_at((5, 6)) is None

    go.apply_move((6, 7))
    assert go.piece_at((6, 7)) == 1
    assert go.piece_at((5, 7)) is None

    go.apply_move((6, 6))
    assert go.piece_at((6, 6)) == 2
    assert go.piece_at((6, 7)) is None

    assert go.legal_move((5, 6)), (
        "Placing a black piece in (5, 6) does not violate the ko rule, "
        "but legal_move() returned False"
    )

    # Check that the move actually happens correctly
    go.apply_move((5, 6))
    for row in range(go.size):
        for col in range(go.size):
            if (row, col) == (5, 6):
                assert go.piece_at((row, col)) == 1
            else:
                assert go.piece_at((row, col)) is None


def test_superko_1() -> None:
    """
    Check that the superko rule is enforced. We make the same
    moves as test_ko_2 and, since that results in a prior state,
    placing the final black piece in (5, 6) should not be allowed.
    """
    go = GoFake(19, 2, superko=True)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    go.apply_move((5, 7))
    assert go.piece_at((5, 7)) == 2
    assert go.piece_at((5, 6)) is None

    go.apply_move((6, 7))
    assert go.piece_at((6, 7)) == 1
    assert go.piece_at((5, 7)) is None

    go.apply_move((6, 6))
    assert go.piece_at((6, 6)) == 2
    assert go.piece_at((6, 7)) is None

    assert not go.legal_move((5, 6)), (
        "Placing a black piece in (5, 6) violates the superko rule, "
        "but legal_move() returned True"
    )


def test_available_moves_1() -> None:
    """
    Test that available_moves returns all the intersections
    in an empty game
    """
    go = GoFake(19, 2)

    moves = go.available_moves

    assert len(moves) == 19 * 19
    for row in range(go.size):
        for col in range(go.size):
            assert (row, col) in moves


def test_available_moves_2() -> None:
    """
    Test that available_moves returns all the intersections
    in a game after a few moves (none of these moves will
    result in a capture, so the ko rule won't apply)
    """
    initial_moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (13, 2),
    ]

    go = GoFake(19, 2)

    for move in initial_moves:
        go.apply_move(move)

    moves = go.available_moves

    assert len(moves) == 19 * 19 - len(initial_moves)
    for row in range(go.size):
        for col in range(go.size):
            pos = (row, col)
            if pos in initial_moves:
                assert pos not in moves
            else:
                assert pos in moves


def test_pass_1() -> None:
    """
    Test that passing the turn updates the turn correctly
    (on an empty board)
    """
    go = GoFake(19, 2)

    assert go.turn == 1
    go.pass_turn()
    assert go.turn == 2


def test_pass_2() -> None:
    """
    Test that passing the turn updates the turn correctly
    (on a board with a few pieces on it, and where it
    is player 2's turn)
    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((6, 6))
    go.apply_move((7, 7))
    go.pass_turn()
    assert go.turn == 1


def test_pass_3() -> None:
    """
    Test that having both players pass consecutively ends the game
    (starting from an empty board)
    """
    go = GoFake(19, 2)

    go.pass_turn()
    go.pass_turn()
    assert go.done


def test_pass_4() -> None:
    """
    Test that having both players pass consecutively ends the game
    (on a board with a few pieces on it, and where it
    is player 2's turn)
    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((6, 6))
    go.apply_move((7, 7))
    go.pass_turn()
    go.pass_turn()
    assert go.done


def test_pass_5() -> None:
    """
    Test that having both players pass, but with a move
    between the passes does *not* end the game.
    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((6, 6))
    go.apply_move((7, 7))
    go.pass_turn()
    go.apply_move((8, 8))
    go.pass_turn()
    assert not go.done


def test_fake_end_1() -> None:
    """
    Test that the fake mechanism for ending a game
    (placing a piece in position 0, 0) works correctly
    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((6, 6))
    go.apply_move((7, 7))
    go.apply_move((8, 8))
    go.apply_move((0, 0))

    assert go.done


def test_fake_end_2() -> None:
    """
    Test that the fake mechanism for ending a game
    (placing a piece in position 0, 0) works correctly,
    and that it specifically ends the game immediately,
    without processing any captures.
    """
    go = GoFake(19, 2)

    go.apply_move((1, 0))
    go.apply_move((0, 0))

    assert go.done

    assert go.piece_at((1, 0)) == 1


def test_fake_end_3() -> None:
    """
    Test that the fake mechanism for ending a game
    (placing a piece in position 0, 0) works correctly,
    and that all empty positions are filled with the piece
    that was placed in (0, 0)
    """
    go = GoFake(19, 2)

    # Place a few pieces, and end the game
    # by placing a piece in (0, 0)
    initial_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (0, 0)]
    for move in initial_moves:
        go.apply_move(move)

    assert go.done

    # Check that the pieces we placed are still there:
    assert go.piece_at((1, 1)) == 1
    assert go.piece_at((2, 2)) == 2
    assert go.piece_at((3, 3)) == 1
    assert go.piece_at((4, 4)) == 2
    assert go.piece_at((0, 0)) == 1

    # All other positions should be filled with the
    # player that ended the game (1)
    for row in range(go.size):
        for col in range(go.size):
            pos = (row, col)
            if pos in initial_moves:
                continue
            assert go.piece_at(pos) == 1


def test_scores_1() -> None:
    """
    Check the scores for an empty board (0 points per player)
    """
    go = GoFake(19, 2)

    scores = go.scores()

    assert scores[1] == 0
    assert scores[2] == 0


def test_scores_2() -> None:
    """
    Check the scores for the following board:

         4  5  6  7  8  9
      4  ·  ·  ·  ·  ·  ·
      5  ·  B  B  ·  W  ·
      6  ·  ·  ·  ·  ·  ·

    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((5, 8))
    go.apply_move((5, 6))

    scores = go.scores()

    assert scores[1] == 2
    assert scores[2] == 1


def test_outcome_1() -> None:
    """
    Check the outcome for an empty board (0 points per player),
    """
    go = GoFake(19, 2)

    go.pass_turn()
    go.pass_turn()

    assert go.outcome == [1, 2]


def test_outcome_2() -> None:
    """
    Check the outcome for the following board (black wins):

         4  5  6  7  8  9
      4  ·  ·  ·  ·  ·  ·
      5  ·  B  B  ·  W  ·
      6  ·  ·  ·  ·  ·  ·
    """
    go = GoFake(19, 2)

    go.apply_move((5, 5))
    go.apply_move((5, 8))
    go.apply_move((5, 6))
    go.pass_turn()
    go.pass_turn()

    assert go.outcome == [1]


def test_outcome_3() -> None:
    """
    Check the outcome for the following board (white wins):

         4  5  6  7  8  9
      4  ·  ·  ·  ·  ·  ·
      5  ·  ·  B  ·  W  W
      6  ·  ·  ·  ·  ·  ·
    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    go.apply_move((5, 8))
    go.pass_turn()
    go.apply_move((5, 9))
    go.pass_turn()
    go.pass_turn()

    assert go.outcome == [2]


def test_outcome_4() -> None:
    """
    Check the outcome for the following board (tie):

         4  5  6  7  8  9
      4  ·  ·  ·  ·  ·  ·
      5  ·  ·  B  ·  W  ·
      6  ·  ·  B  ·  W  ·
    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    go.apply_move((5, 8))
    go.apply_move((6, 6))
    go.apply_move((6, 8))
    go.pass_turn()
    go.pass_turn()

    assert go.outcome == [1, 2]


def test_simulate_move_1() -> None:
    """
    Test that simulating a move creates a new game
    """

    go = GoFake(19, 2)

    new_go = go.simulate_move((5, 5))

    # Check that the original Go object has not been modified
    assert go.piece_at((5, 5)) is None
    assert go.turn == 1

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 5)) == 1
    assert new_go.turn == 2


def test_simulate_move_2() -> None:
    """
    After making a few moves, check that simulating a move
    correctly creates a new game.
    """
    initial_moves = [
        (3, 3),
        (6, 16),
        (1, 1),
        (13, 0),
        (16, 1),
        (18, 15),
        (13, 14),
        (2, 10),
        (1, 17),
        (3, 13),
        (11, 2),
        (2, 8),
        (13, 11),
        (11, 0),
        (4, 17),
        (3, 6),
        (16, 2),
        (5, 2),
        (14, 8),
        (13, 2),
    ]

    go = GoFake(19, 2)

    for move in initial_moves:
        go.apply_move(move)

    new_go = go.simulate_move((5, 5))

    # Check that the original GoFake object has not been modified
    assert go.piece_at((5, 5)) is None
    for move in initial_moves:
        assert go.piece_at(move) is not None
    assert go.turn == 1

    # Check that the move was applied in the new GoFake object
    assert new_go.piece_at((5, 5)) == 1
    for move in initial_moves:
        assert new_go.piece_at(move) is not None
    assert new_go.turn == 2


def test_simulate_move_3() -> None:
    """
    We place one piece in position (5, 6) and then
    simulate placing a piece in position (5, 7).
    The piece in position (5, 6) should be captured
    (but only in the new game created by simulate_move)
    """
    go = GoFake(19, 2)

    go.apply_move((5, 6))
    assert go.piece_at((5, 6)) == 1

    new_go = go.simulate_move((5, 7))

    # Check that the original Go object has not been modified
    assert go.piece_at((5, 6)) == 1
    assert go.piece_at((5, 7)) is None
    assert go.turn == 2

    # Check that the move was applied in the new Go object
    assert new_go.piece_at((5, 6)) is None
    assert new_go.piece_at((5, 7)) == 2
    assert new_go.turn == 1


def test_simulate_move_4() -> None:
    """
    Check that simulating a pass works correctly.
    """
    go = GoFake(19, 2)

    new_go = go.simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1

    # Check that the pass was applied in the new Go object
    assert new_go.turn == 2


def test_simulate_move_5() -> None:
    """
    Check that simulating two consecutive passes works correctly.
    """
    go = GoFake(19, 2)

    new_go = go.simulate_move(None).simulate_move(None)

    # Check that the original Go object has not been modified
    assert go.turn == 1
    assert not go.done

    # Check that the passes were applied in the new Go object
    assert new_go.done
