import pytest
from unittest.mock import patch
from question_two.wheel_of_fortune import spin_wheel, display_word, play_game

# Test: spin_wheel
def test_spin_wheel_returns_valid_value():
    for _ in range(100):
        value = spin_wheel()
        assert value in [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

# Test: display_word
@pytest.mark.parametrize("word, guessed, expected", [
    ("hello", set(), "_ _ _ _ _"),
    ("hello", {"h"}, "h _ _ _ _"),
    ("hello world", {"l", "o"}, "_ _ l l o   _ o _ l _"),
    ("test", {"t", "e", "s"}, "t e s t"),
])
def test_display_word(word, guessed, expected):
    assert display_word(word, guessed) == expected

# Test: play_game (mocked)
@patch("builtins.input")
@patch("question_two.wheel_of_fortune.spin_wheel")
def test_play_game_win_case(mock_spin, mock_input, capsys):
    # Setup mock values
    mock_input.side_effect = [
        "hello",   # phrase input
        "h",       # correct guess
        "e",       # correct guess
        "l",       # correct guess
        "o"        # correct guess → completes the word
    ]
    mock_spin.return_value = 100  # Fixed point value for simplicity

    play_game()

    captured = capsys.readouterr().out

    assert "Congratulations!" in captured
    assert "hello" in captured
    assert "Total points:" in captured
    assert "Wheel spin! You got: 100 points." in captured

@patch("builtins.input")
@patch("question_two.wheel_of_fortune.spin_wheel")
def test_play_game_invalid_inputs(mock_spin, mock_input, capsys):
    mock_spin.return_value = 200

    mock_input.side_effect = [
        "",              # empty phrase
        "123!",          # invalid phrase
        "hangman",       # valid phrase

        "1",             # invalid letter
        "a",             # valid
        "a",             # repeated → now triggers expected message
        "h",
        "n",
        "g",
        "m"
    ]

    play_game()

    captured = capsys.readouterr().out
    assert "Word or phrase cannot be empty." in captured
    assert "Only words or phrases are allowed." in captured
    assert "Please enter a valid letter." in captured
    assert "You already guessed that letter." in captured

