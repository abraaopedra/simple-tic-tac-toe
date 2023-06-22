import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font

# We will use object-oriented programming, so we define a class for our game
class TicTacToeGUI:
    # The __init__ method is the constructor, it's the first method that's called when you create a new object
    def __init__(self, root):
        # Store the tkinter root widget as an instance variable
        self.root = root
        # Set the title of the window
        self.root.title("Tic Tac Toe Game")
        # Set the size of the window
        self.root.geometry("500x500")
        # Set the background color
        self.root.configure(bg='lightblue')

        # Initialize the game variables
        self.players = ["Player 1", "Player 2"]
        self.scores = {player: 0 for player in self.players}
        self.current_player = 0
        self.best_of = 3
        self.board = [' ']*9
        self.buttons = []
        self.score_label = None
        # Show the start page
        self.start_page()

    # Method for creating the start page
    def start_page(self):
        # Create a frame for the form
        form = tk.Frame(self.root)
        form.pack(padx=50, pady=50)

        # Add labels and entry fields for player names
        ttk.Label(form, text = "Player 1:", font = ('Verdana', 10)).grid(column = 0, row = 0, padx = 10, pady = 25)
        ttk.Label(form, text = "Player 2:", font = ('Verdana', 10)).grid(column = 0, row = 1, padx = 10, pady = 25)
        p1_name = ttk.Entry(form)
        p1_name.grid(column = 1, row = 0, padx = 10, pady = 25)
        p2_name = ttk.Entry(form)
        p2_name.grid(column = 1, row = 1, padx = 10, pady = 25)

        # Add a label and a dropdown for the game type
        ttk.Label(form, text = "Game Type", font = ('Verdana', 10)).grid(column = 0, row = 2, padx = 10, pady = 25)
        game_type = ttk.Combobox(form, values=["Best of 1", "Best of 3", "Best of 5", "Best of 7"])
        game_type.grid(column = 1, row = 2, padx = 10, pady = 25)

        # Add a button that will submit the form
        submit_button = ttk.Button(form, text = "Submit", command = lambda: self.get_start_info(p1_name, p2_name, game_type))
        submit_button.grid(column = 0, row = 3, padx = 10, pady = 25, columnspan = 2)

    # Method for processing the start page form
    def get_start_info(self, p1_entry, p2_entry, game_type_entry):
        # Get the entered values
        p1_name = p1_entry.get() or "Player 1"
        p2_name = p2_entry.get() or "Player 2"
        game_type = game_type_entry.get()

        # Update the game variables with the entered values
        self.players = [p1_name, p2_name]
        self.scores = {player: 0 for player in self.players}
        self.best_of = int(game_type[-1]) if game_type else 3

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Build the game interface
        self.build_gui()

    # Method for building the game interface
    def build_gui(self):
        # Create a frame for the game area
        game_area = tk.Frame(self.root)
        game_area.pack(fill='both', expand=True)

        # Create the buttons for the board
        for i in range(3):
            game_area.rowconfigure(i, weight=1)
            row = []
            for j in range(3):
                game_area.columnconfigure(j, weight=1)
                button = tk.Button(game_area, text=" ", command=lambda i=i, j=j: self.make_move(i, j), bg='white')
                button.grid(row=i, column=j, sticky='nsew')
                row.append(button)
            self.buttons.append(row)

        # Create a label for the score
        self.score_label = tk.Label(self.root, text = self.get_score_text(), font = ('Verdana', 10), bg='lightblue')
        self.score_label.pack(pady=20)

    # Method for making a move
    def make_move(self, i, j):
        # If the button is not pressed yet
        if self.board[i*3+j] == ' ':
            # Update the board and the button text
            self.board[i*3+j] = 'X' if self.current_player == 0 else 'O'
            self.buttons[i][j]['text'] = self.board[i*3+j]
            # Disable the button so it can't be pressed again
            self.buttons[i][j]['state'] = tk.DISABLED
            self.buttons[i][j]['font'] = Font(size=min(self.root.winfo_height(), self.root.winfo_width())//10)

            # Check if the game is over
            winner = self.check_winner()
            if winner is not None:
                # If the game is over, update the score and show a message
                self.scores[winner] += 1
                messagebox.showinfo("Game Over", f"{winner} won!")
                if max(self.scores.values()) < self.best_of//2 + 1:
                    # If the match is not over, ask for the next action
                    self.ask_for_next_action()
                else:
                    # If the match is over, show a message and ask for the next action
                    messagebox.showinfo("Match Over", f"{winner} has won the best-of-{self.best_of}!")
                    self.ask_for_next_action(end_match=True)
            elif ' ' not in self.board:
                # If the game is a draw, show a message and ask for the next action
                messagebox.showinfo("Game Over", "It's a draw!")
                self.ask_for_next_action()
            else:
                # If the game is not over, switch the current player
                self.current_player = 1 - self.current_player
                self.score_label.config(text=self.get_score_text())

    # Method for getting the score text
    def get_score_text(self):
        return f"{self.players[0]}: {self.scores[self.players[0]]} | {self.players[1]}: {self.scores[self.players[1]]} | {self.players[self.current_player]}'s turn"

    # Method for checking if the game is over
    def check_winner(self):
        # List of winning positions
        win_positions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for wp in win_positions:
            # If one of the winning positions is occupied by the same player
            if self.board[wp[0]] == self.board[wp[1]] == self.board[wp[2]] != ' ':
                # Return the winner
                return self.players[0] if self.board[wp[0]] == 'X' else self.players[1]
        # If there's no winner, return None
        return None

    # Method for resetting the board
    def reset_board(self):
        # Reset the board and the buttons
        self.board = [' ']*9
        for i in range(3):
            for j in range(3):
                self.buttons[i][j]['text'] = ' '
                self.buttons[i][j]['state'] = tk.NORMAL
        self.score_label.config(text=self.get_score_text())

    # Method for asking for the next action
    def ask_for_next_action(self, end_match=False):
        # Ask if the player wants to play again or return to the start page
        response = messagebox.askyesnocancel("Next action", "Do you want to play again?" if not end_match else "Do you want to start a new match?")
        if response is True:
            self.reset_board()
        elif response is False:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.start_page()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToeGUI(root)
    root.mainloop()
