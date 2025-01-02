import sys


def clear_input_after_enter(prompt):
    user_input = input(prompt)  # Get user input
    # Move cursor up one line and clear the line
    sys.stdout.write("\033[F\033[K")
    sys.stdout.flush()
    return user_input
