import tkinter as tk
from tkinter import messagebox
import threading
import time

EMPTY, BLACK, WHITE = 0, -1, 1

def initial_board():
    board = [[EMPTY for _ in range(8)] for _ in range(8)]
    board[3][3], board[4][4] = WHITE, WHITE
    board[3][4], board[4][3] = BLACK, BLACK
    return board

def print_board(board):
    print("  " + " ".join(str(i) for i in range(8)))
    for i, row in enumerate(board):
        print(i, end=" ")
        for cell in row:
            if cell == BLACK:
                print("○", end=" ")
            elif cell == WHITE:
                print("●", end=" ")
            else:
                print(".", end=" ")
        print()

def valid_moves(board, player):
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]
    moves = []
    for x in range(8):
        for y in range(8):
            if board[x][y] != EMPTY:
                continue
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                found_opponent = False
                while 0 <= nx < 8 and 0 <= ny < 8:
                    if board[nx][ny] == -player:
                        found_opponent = True
                    elif board[nx][ny] == player and found_opponent:
                        moves.append((x, y))
                        break
                    else:
                        break
                    nx += dx
                    ny += dy
    return list(set(moves))

def apply_move(board, move, player):
    x, y = move
    new_board = [row[:] for row in board]
    new_board[x][y] = player

    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        path = []
        while 0 <= nx < 8 and 0 <= ny < 8:
            if new_board[nx][ny] == -player:
                path.append((nx, ny))
            elif new_board[nx][ny] == player:
                for px, py in path:
                    new_board[px][py] = player
                break
            else:
                break
            nx += dx
            ny += dy
    return new_board

def evaluate(board, player):
    score = 0
    for row in board:
        for cell in row:
            score += cell
    return player * score

def game_over(board):
    return not valid_moves(board, BLACK) and not valid_moves(board, WHITE)


def minimax_ab(board, depth, alpha, beta, maximizing_player, player):
    if depth == 0 or game_over(board):
        return evaluate(board, player), None

    valid = valid_moves(board, player if maximizing_player else -player)

    if not valid:
        return evaluate(board, player), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in valid:
            new_board = apply_move(board, move, player)
            eval, _ = minimax_ab(new_board, depth-1, alpha, beta, False, player)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in valid:
            new_board = apply_move(board, move, -player)
            eval, _ = minimax_ab(new_board, depth-1, alpha, beta, True, player)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move



CELL = 60
PADDING = 20
BOARD_SIZE = 8 * CELL + 2 * PADDING

class OthelloGUI:
    def __init__(self, root):
        self.root = root
        root.title("Othello / Reversi")
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="#2b6b2b")
        self.canvas.pack()

        self.status = tk.Label(root, text="", font=("Arial", 12))
        self.status.pack(pady=6)

        control_frame = tk.Frame(root)
        control_frame.pack(pady=4)
        tk.Label(control_frame, text="AI depth:").pack(side=tk.LEFT)
        self.depth_var = tk.IntVar(value=3)
        tk.Spinbox(control_frame, from_=1, to=6, width=3, textvariable=self.depth_var).pack(side=tk.LEFT, padx=4)
        tk.Button(control_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=6)
        tk.Button(control_frame, text="Pass (for human)", command=self.human_pass).pack(side=tk.LEFT, padx=6)

        self.board = initial_board()
        self.current_player = BLACK  # human = BLACK, AI = WHITE
        self.ai_thinking = False

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()
        self.update_status()

    def new_game(self):
        if self.ai_thinking:
            return
        self.board = initial_board()
        self.current_player = BLACK
        self.draw_board()
        self.update_status()

    def human_pass(self):
        if self.ai_thinking:
            return
        moves = valid_moves(self.board, self.current_player)
        if moves:
            messagebox.showinfo("Pass not allowed", "شما هنوز حرکت دارید.")
            return
        self.current_player *= -1
        self.draw_board()
        self.update_status()
        self.root.after(50, self.maybe_ai_move)

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(8):
            for j in range(8):
                x1 = PADDING + j * CELL
                y1 = PADDING + i * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#2b6b2b", outline="#1e4b1e")
        for i in range(8):
            for j in range(8):
                v = self.board[i][j]
                if v != EMPTY:
                    self.draw_disc(i, j, v)

        moves = valid_moves(self.board, self.current_player)
        for (x, y) in moves:
            cx = PADDING + y * CELL + CELL//2
            cy = PADDING + x * CELL + CELL//2
            r = 6
            self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#ffd54f", outline="")

    def draw_disc(self, i, j, v):
        x1 = PADDING + j * CELL + 6
        y1 = PADDING + i * CELL + 6
        x2 = x1 + CELL - 12
        y2 = y1 + CELL - 12
        if v == BLACK:
            self.canvas.create_oval(x1, y1, x2, y2, fill="black", outline="white")
        elif v == WHITE:
            self.canvas.create_oval(x1, y1, x2, y2, fill="white", outline="black")

    def on_click(self, event):
        if self.ai_thinking:
            return
        px, py = event.y - PADDING, event.x - PADDING
        if px < 0 or py < 0:
            return
        i = px // CELL
        j = py // CELL
        if not (0 <= i < 8 and 0 <= j < 8):
            return
        move = (i, j)
        moves = valid_moves(self.board, self.current_player)
        if move in moves and self.current_player == BLACK:
            self.board = apply_move(self.board, move, self.current_player)
            self.current_player *= -1
            self.draw_board()
            self.update_status()
            self.root.after(50, self.maybe_ai_move)
        else:
            self.status.flash = getattr(self.status, "flash", 0) + 1
            self.update_status(temp="حرکت نامعتبر")

    def update_status(self, temp=None):
        if temp:
            txt = temp
        else:
            human = "● (شما)" if self.current_player == BLACK else "○ (شما)"
            ai = "○ (AI)" if self.current_player == WHITE else "● (AI)"
            moves = valid_moves(self.board, self.current_player)
            if self.ai_thinking:
                txt = "AI در حال تصمیم‌گیری..."
            elif not moves:
                txt = f"بازیکن {'●' if self.current_player==BLACK else '○'} هیچ حرکتی ندارد. (پاس)"
            else:
                txt = f"نوبت {'شما (●)' if self.current_player==BLACK else 'AI (○)'} — حرکات مجاز: {len(moves)}"
        self.status.config(text=txt)

    def maybe_ai_move(self):
        if self.ai_thinking:
            return
        if self.current_player == WHITE:
            moves = valid_moves(self.board, WHITE)
            if not moves:
                self.current_player *= -1
                self.draw_board()
                self.update_status()
                return
            self.ai_thinking = True
            self.update_status()
            threading.Thread(target=self.run_ai_move, daemon=True).start()

    def run_ai_move(self):
        depth = max(1, int(self.depth_var.get()))
        score, move = minimax_ab(self.board, depth, float('-inf'), float('inf'), True, WHITE)
        def on_done():
            if move:
                self.board = apply_move(self.board, move, WHITE)
            self.current_player *= -1
            self.ai_thinking = False
            self.draw_board()
            self.update_status()
            if game_over(self.board):
                self.show_result()
        self.root.after(10, on_done)

    def show_result(self):
        black_score = sum(row.count(BLACK) for row in self.board)
        white_score = sum(row.count(WHITE) for row in self.board)
        if black_score > white_score:
            msg = f"شما برنده شدید! ●={black_score}  ○={white_score}"
        elif white_score > black_score:
            msg = f"کامپیوتر برنده شد. ○={white_score}  ●={black_score}"
        else:
            msg = f"مساوی شد. ●={black_score}  ○={white_score}"
        messagebox.showinfo("نتیجه بازی", msg)

if __name__ == "__main__":
    root = tk.Tk()
    gui = OthelloGUI(root)
    root.mainloop()
