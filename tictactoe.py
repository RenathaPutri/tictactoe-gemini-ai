import json
import random
import time
import google.generativeai as genai
from colorama import Fore, Style

# Configure Gemini AI API Key
genai.configure(api_key="")

def print_board(board):
    print(Fore.CYAN + "\n Tic-Tac-Toe Board")
    print(Fore.YELLOW + " " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8] + Style.RESET_ALL)

def check_winner(board, player):
    win_conditions = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)

def ai_move(board, difficulty):
    model = genai.GenerativeModel("gemini-pro")
    available_moves = [i for i in range(9) if board[i] not in ('X', 'O')]
    if difficulty == "easy":
        return random.choice(available_moves)
    elif difficulty == "hard":
        prompt = f"Given the Tic-Tac-Toe board {board}, what is the best move? Choose from {available_moves}."
        response = model.generate_content(prompt)
        try:
            move = int(response.text.strip())
            if move in available_moves:
                return move
        except ValueError:
            pass
    return random.choice(available_moves) if available_moves else None

def save_score(result):
    try:
        with open("score.json", "r") as file:
            scores = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        scores = {"Wins": 0, "Losses": 0, "Draws": 0}
    
    scores[result] += 1
    
    with open("score.json", "w") as file:
        json.dump(scores, file)

def load_score():
    try:
        with open("score.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"Wins": 0, "Losses": 0, "Draws": 0}

def undo_move(board, history):
    if history:
        last_move = history.pop()
        board[last_move] = str(last_move + 1)
        return True
    return False

def multiplayer_game():
    board = [str(i + 1) for i in range(9)]
    history = []
    players = ['X', 'O']
    turn = 0
    print("Multiplayer mode: Player 1 (X) vs Player 2 (O)")
    
    for _ in range(9):
        print_board(board)
        move = int(input(f"Player {players[turn % 2]}, enter your move (1-9): ")) - 1
        while board[move] in ('X', 'O'):
            move = int(input("Invalid move. Enter again: ")) - 1
        
        board[move] = players[turn % 2]
        history.append(move)
        
        if check_winner(board, players[turn % 2]):
            print_board(board)
            print(Fore.GREEN + f"Player {players[turn % 2]} wins!" + Style.RESET_ALL)
            return
        
        turn += 1
    
    print_board(board)
    print(Fore.BLUE + "It's a draw!" + Style.RESET_ALL)

def play_game():
    board = [str(i + 1) for i in range(9)]
    user_symbol, ai_symbol = ('X', 'O') if random.choice([True, False]) else ('O', 'X')
    history = []
    mode = input("Choose mode (singleplayer/multiplayer): ").strip().lower()
    if mode == "multiplayer":
        multiplayer_game()
        return
    difficulty = input("Choose difficulty (easy/medium/hard): ").strip().lower()
    print(f"You are {user_symbol}, AI is {ai_symbol}")
    
    for turn in range(9):
        print_board(board)
        if (turn % 2 == 0 and user_symbol == 'X') or (turn % 2 == 1 and user_symbol == 'O'):
            move = int(input("Enter your move (1-9): ")) - 1
            while board[move] in ('X', 'O'):
                move = int(input("Invalid move. Enter again: ")) - 1
        else:
            print("AI is thinking...")
            time.sleep(1)
            move = ai_move(board, difficulty)
        
        board[move] = user_symbol if turn % 2 == 0 else ai_symbol
        history.append(move)
        
        if check_winner(board, user_symbol if turn % 2 == 0 else ai_symbol):
            print_board(board)
            if turn % 2 == 0:
                print(Fore.GREEN + "Congratulations! You win!" + Style.RESET_ALL)
                save_score("Wins")
            else:
                print(Fore.RED + "AI wins! Better luck next time." + Style.RESET_ALL)
                save_score("Losses")
            return
    
    print_board(board)
    print(Fore.BLUE + "It's a draw!" + Style.RESET_ALL)
    save_score("Draws")

def main():
    print("Welcome to Tic-Tac-Toe!")
    while True:
        play_game()
        scores = load_score()
        print(f"Scores - Wins: {scores['Wins']}, Losses: {scores['Losses']}, Draws: {scores['Draws']}")
        play_again = input("Do you want to play again? (y/n): ").lower()
        if play_again != 'y':
            break

if __name__ == "__main__":
    main()
