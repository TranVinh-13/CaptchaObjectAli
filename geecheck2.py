from collections import deque
def check(board):
    rows = len(board)
    cols = len(board[0])
    for row in board:
        for i in range(cols - 2):
            if row[i] == row[i + 1] == row[i + 2]:
                return True
    for col in range(cols):
        for i in range(rows - 2):
            if board[i][col] == board[i + 1][col] == board[i + 2][col]:
                return True
    return False
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
def bfs_modify_board(board):
    rows = len(board)
    cols = len(board[0])
    queue = deque([(board, None)]) 
    visited = set()
    visited.add(tuple(map(tuple, board))) 
    while queue:
        current_board, last_move = queue.popleft()
        if check(current_board):
            return current_board
        for i in range(rows):
            for j in range(cols):
                for dx, dy in DIRECTIONS:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols:
                        new_board = [row[:] for row in current_board]
                        new_board[i][j], new_board[ni][nj] = new_board[ni][nj], new_board[i][j] 
                        if tuple(map(tuple, new_board)) not in visited:
                            visited.add(tuple(map(tuple, new_board)))
                            queue.append((new_board, (i, j)))  
    return None 
def print_diff(board1, board2):
    rows = len(board1)
    cols = len(board1[0])
    res = []
    for i in range(rows):
        for j in range(cols):
            if board1[i][j] != board2[i][j]:
                res.append((i,j))
    return res

board = [
    [1, 1, 2],
    [3, 1, 2],
    [2, 3, 3]
]
modified_board = bfs_modify_board(board)
if modified_board:
    print("Bảng sau khi chỉnh sửa:")
    for row in modified_board:
        print(row)
else:
    print("Không tìm thấy bảng có chiến thắng.")
print(print_diff(board,modified_board))