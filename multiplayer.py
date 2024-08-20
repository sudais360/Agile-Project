import random
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import MySQLdb
class QuizGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Geography Quiz Game")

        self.current_question = 0
        self.score = 0

        self.colors = ["red", "green", "blue", "yellow"]  # Add colors
        self.symbols = ["❤", "✨", "🌟", "🎉", "🔥"]  # Add symbols

        self.start_button = tk.Button(self.root, text="Start Game", command=self.start_multiplayer)
        self.start_button.pack()
    def load_questions_from_db(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="sudais22", db="quiz_game")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM questions ORDER BY RAND();")
        rows = cursor.fetchall()
        db.close()

        self.questions = []
        for row in rows:
            question_data = {
                'question': row[1],
                'options': [row[2], row[3], row[4]],
                'correct_answer': row[5]
            }
            self.questions.append(question_data)
    def start_multiplayer(self):
        print("start_multiplayer called")
        self.start_button.destroy()
        self.load_questions_from_db()

        num_players = simpledialog.askinteger("Number of Players", "Enter the number of players:")
        if num_players:
            self.players = {}
            for i in range(num_players):
                player_name = simpledialog.askstring(f"Player {i + 1}", f"Enter name for player {i + 1}:")
                if player_name:
                    color = self.colors[i % len(self.colors)]
                    symbol_choice = simpledialog.askinteger("Symbol Choice",
                                                            f"Choose a symbol for {player_name}:\n1. ❤\n2. ✨\n3. 🌟\n4. 🎉\n5. 🔥")
                    if 1 <= symbol_choice <= 5:
                        self.players[player_name] = {"color": color, "symbol": self.symbols[symbol_choice - 1],
                                                     "score": 0}

            self.current_player = list(self.players.keys())[0]
            self.frame = tk.Frame(self.root)
            self.frame.pack()
            self.update_question()

    def update_question(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        if self.current_question < len(self.questions):
            question_data = self.questions[self.current_question]
            self.question_label = tk.Label(self.frame,
                                           text=f"{question_data['question']}\n\nFor Player: {self.current_player}",
                                           font=("Helvetica", 16))
            self.question_label.pack(pady=20)

            self.option_buttons = []
            for i in range(4):
                button = tk.Button(self.frame, text=question_data['options'][i], font=("Helvetica", 12),
                                   command=lambda i=i: self.answer_question(i))
                button.pack(pady=5)
                self.option_buttons.append(button)

            if hasattr(self, "players"):
                self.root.configure(bg=self.players[self.current_player]["color"])

        else:
            self.show_final_score()

    def answer_question(self, user_answer):
        question_data = self.questions[self.current_question]
        if question_data['options'][user_answer] == question_data['correct_answer']:
            self.players[self.current_player]["score"] += 1
        self.current_question += 1

        for button in self.option_buttons:
            button.destroy()
        self.question_label.destroy()

        if hasattr(self, "players"):
            player_names = list(self.players.keys())
            self.current_player = player_names[(player_names.index(self.current_player) + 1) % len(self.players)]
            if self.current_question < len(self.questions):
                self.root.configure(bg=self.players[self.current_player]["color"])
                print(f"\nNext question for {self.current_player} ({self.players[self.current_player]['symbol']}):")
        self.update_question()

    def show_final_score(self):
        if hasattr(self, "players"):
            final_scores = "\nFinal Scores:\n"
            sorted_players = sorted(self.players.items(), key=lambda x: x[1]['score'], reverse=True)
            highest_score_player = sorted_players[0]
            for rank, (player_name, player_info) in enumerate(sorted_players, start=1):
                final_scores += f"Rank {rank}: {player_name} {player_info['symbol']} - Score: {player_info['score']} points\n"
            print(final_scores)
            self.show_leaderboard(sorted_players)
            self.congratulate_winner(highest_score_player)
        else:
            messagebox.showinfo("Quiz Over", f"Your score: {self.score}")

        self.root.destroy()

    def show_leaderboard(self, sorted_players):
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Leaderboard")

        tree = ttk.Treeview(leaderboard_window, columns=("Rank", "Name", "Score"), show="headings")
        tree.heading("Rank", text="Rank")
        tree.heading("Name", text="Name")
        tree.heading("Score", text="Score")
        for rank, (player_name, player_info) in enumerate(sorted_players, start=1):
            tree.insert("", "end", values=(rank, player_name, player_info['score']))
        tree.pack()

    def congratulate_winner(self, highest_score_player):
        winner_name = highest_score_player[0]
        highest_score = highest_score_player[1]['score']
        messagebox.showinfo("Congratulations!",
                            f"Congratulations {winner_name}!\nYou scored the highest: {highest_score} points.")

if __name__ == "__main__":
    root = tk.Tk()
    game = QuizGame(root)
    root.update_idletasks()
    root.mainloop()
