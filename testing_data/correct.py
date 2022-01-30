# Sudoku Validation

def isValid(arr):
    arr = [each for each in arr if each!='.']
    if len(arr)!=len(set(arr)):
        return False
    return True

def test_Row2arr(board):
    for i in range(len(board)):
        if not isValid(board[i]):
            return False
    return True

def test_col2arr(board):
    for i in range(9):
        arr = []
        for j in range(len(board)):
            arr.append(board[j][i])
        if not isValid(arr):
            return False
    return True

def test_box2arr(board):
    for i in range(0,9,3):
        for j in range(0,9,3):
            arr = board[i][j:j+3]+board[i+1][j:j+3]+board[i+2][j:j+3]
            if not isValid(arr):
                return False
    return True 
            
def isValidSudoku(board):
    # from collections import Counter
    if test_Row2arr(board) and test_col2arr(board) and test_box2arr(board):
        return "Valid"
    else:
        return "Invalid"


rounds = int(input())
for round in range(rounds):
    board = []
    for _ in range(9):
        board.append(input().split())
    print(isValidSudoku(board))
    if round != rounds-1:
        nextLine = input()


