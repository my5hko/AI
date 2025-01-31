import math

# Ініціалізація порожнього ігрового поля
def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

# Перевірка, чи є переможець
def check_winner(board):
    # Перевірка рядків, стовпців та діагоналей
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

# Перевірка, чи гра завершена
def is_full(board):
    return all(cell != " " for row in board for cell in row)

# Функція для оцінки стану гри
def evaluate(board):
    winner = check_winner(board)
    if winner == "X":  # Максимізуючий гравець
        return 1
    elif winner == "O":  # Мінімізуючий гравець
        return -1
    return 0

# Алгоритм мінімакс з альфа-бета відсіканням
def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate(board)
    if score != 0 or is_full(board):  # Якщо гра завершена
        return score
    
    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "X"  # Хід максимізуючого гравця
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"  # Хід мінімізуючого гравця
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Знайти найкращий хід
def best_move(board):
    best_val = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "X"
                move_val = minimax(board, 0, False, -math.inf, math.inf)
                board[i][j] = " "
                if move_val > best_val:
                    best_val = move_val
                    move = (i, j)
    return move

# Основна функція для гри
def play_tic_tac_toe():
    board = create_board()
    while not check_winner(board) and not is_full(board):
        print("Поточний стан поля:")
        for row in board:
            print(" | ".join(row))
        print()
        
        # Хід гравця (O)
        row, col = map(int, input("Введіть рядок і стовпець (0-2) через пробіл: ").split())
        if board[row][col] == " ":
            board[row][col] = "O"
        else:
            print("Некоректний хід. Спробуйте ще раз.")
            continue
        
        if check_winner(board) or is_full(board):
            break
        
        # Хід комп'ютера (X)
        print("Хід комп'ютера:")
        move = best_move(board)
        board[move[0]][move[1]] = "X"
    
    print("Кінцевий стан поля:")
    for row in board:
        print(" | ".join(row))
    winner = check_winner(board)
    if winner:
        print(f"Переможець: {winner}")
    else:
        print("Нічия!")

# Запуск гри
play_tic_tac_toe()