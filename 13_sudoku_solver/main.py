import streamlit as st

st.set_page_config(page_title="Sudoku Solver", page_icon="🧩")
st.title("🧩 Sudoku Solver using Backtracking")

st.markdown("""
### 📝 Instructions:
1. Enter the Sudoku puzzle as a 9x9 grid in the text area below.  
2. Use **spaces** to separate numbers in each row.  
3. Use **0 (zero)** to represent empty cells.  
4. Make sure there are exactly **9 rows**, each containing **9 numbers**.  
5. Once ready, click the **✅ Solve Sudoku** button to see the solution!
""")

# --- Backtracking Sudoku Solver ---
def solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True  # Puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Backtrack

    return False

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return (r, c)
    return None

def is_valid(board, row, col, num):
    # Check row and column
    if num in board[row] or num in (board[i][col] for i in range(9)):
        return False

    # Check 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

# --- Streamlit UI ---
sample_input = """5 3 0 0 7 0 0 0 0
6 0 0 1 9 5 0 0 0
0 9 8 0 0 0 0 6 0
8 0 0 0 6 0 0 0 3
4 0 0 8 0 3 0 0 1
7 0 0 0 2 0 0 0 6
0 6 0 0 0 0 2 8 0
0 0 0 4 1 9 0 0 5
0 0 0 0 8 0 0 7 9"""

user_input = st.text_area(
    "✍️ Enter your Sudoku puzzle below:",
    value=sample_input,
    height=250
)

try:
    board = [[int(x) for x in row.split()] for row in user_input.strip().splitlines()]
    if len(board) != 9 or any(len(row) != 9 for row in board):
        st.error("❌ Please make sure you enter 9 rows with exactly 9 numbers each.")
    else:
        if st.button("✅ Solve Sudoku"):
            board_copy = [row[:] for row in board]
            if solve_sudoku(board_copy):
                st.success("🎉 Solved Sudoku:")
                st.table(board_copy)
            else:
                st.error("🚫 No valid solution found.")
except Exception as e:
    st.error(f"Invalid input: {e}")


# footer
st.markdown("---")
st.caption('Developed with ❤️ using Python and Streamlit by Muhammad Yousaf | Powered by the <a href="https://myousaf-codes.vercel.app" target="_blank">MYousaf-Codes</a>', unsafe_allow_html=True)
