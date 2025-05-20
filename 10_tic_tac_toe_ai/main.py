import streamlit as st

st.set_page_config(page_title="TIC TAC AI", page_icon="🎮")
st.title("🎮 Tic Tac Toe AI")
st.markdown("**AI:** O  |  **You:** X")
st.text("Double click for better experience")

# session
if "board" not in st.session_state:
    st.session_state.board = [None] * 9
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# game
WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
SCORES = {"X": -1, "O": 1, None: 0}

def check_winner(b):
    for i, j, k in WIN_LINES:
        if b[i] and b[i] == b[j] == b[k]:
            return b[i]
    return None

def minimax(b, is_max):
    winner = check_winner(b)
    if winner or None not in b:
        return SCORES[winner]
    best = float('-inf') if is_max else float('inf')
    for i in range(9):
        if b[i] is None:
            b[i] = "O" if is_max else "X"
            score = minimax(b, not is_max)
            b[i] = None
            best = max(best, score) if is_max else min(best, score)
    return best

def get_ai_move(b):
    best_score, move = float('-inf'), None
    for i in range(9):
        if b[i] is None:
            b[i] = "O"
            score = minimax(b, False)
            b[i] = None
            if score > best_score:
                best_score, move = score, i
    return move

def reset():
    st.session_state.board = [None] * 9
    st.session_state.game_over = False

# custom css styleing
st.markdown("""
<style>
/* ... keep your existing button & board styles above ... */

.control-buttons {
  display: flex;        
  flex-direction: row; 
  gap: 1rem;   
  justify-content: center;
  margin-top: 1rem;
}

.control-buttons button {
  width: 140px;       /* same width */
  height: 36px;       /* shorter height */
  font-size: 14px;
  padding: 0;         /* no vertical padding to keep height tight */
  border-radius: 4px;
  background: #444;
  color: #fff;
  transition: background 0.2s;
}
.control-buttons button:hover {
  background: #555;
}
</style>
""", unsafe_allow_html=True)

def end_game(msg, style_method):
    st.session_state.game_over = True
    getattr(st, style_method)(msg)

# board for game
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row * 3 + col
        val = st.session_state.board[idx]
        disabled = (val is not None) or st.session_state.game_over

        with cols[col]:
            if st.button(val or " ", key=idx, disabled=disabled, use_container_width=True):

                st.session_state.board[idx] = "X"
                if (w := check_winner(st.session_state.board)) or None not in st.session_state.board:
                    end_game(
                        "🎉 You win!" if w=="X" else "🤝 It's a tie!",
                        "success" if w=="X" else "info"
                    )
                    break

                ai_idx = get_ai_move(st.session_state.board)
                if ai_idx is not None:
                    st.session_state.board[ai_idx] = "O"

                if (w := check_winner(st.session_state.board)) or None not in st.session_state.board:
                    end_game(
                        "😔 AI wins!" if w=="O" else "🤝 It's a tie!",
                        "error" if w=="O" else "info"
                    )
                    break
    else:
        continue  # runs if inner loop did not break
    break       # break loop if game ended

# end buttons
st.markdown('<div class="control-buttons">', unsafe_allow_html=True)
if st.button("🎮 Play Again"):
    reset()
if st.button("🔁 Reset Game"):
    reset()
st.markdown('</div>', unsafe_allow_html=True)


# footer
st.markdown("---")
st.caption('Developed with ❤️ using Python and Streamlit by Muhammad Yousaf | Powered by the <a href="https://myousaf-codes.vercel.app" target="_blank">MYousaf-Codes</a>', unsafe_allow_html=True)
