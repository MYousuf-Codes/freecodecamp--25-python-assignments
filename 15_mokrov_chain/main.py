import streamlit as st
import random

st.title("🎶 Markov Chain Text Composer")
st.markdown("""
Welcome to the **Markov Chain Text Composer**!  
This tool uses AI principles to generate new text based on your input — ideal for remixing song lyrics, poems, or any kind of creative writing.

---

**How to Use:**
1. Paste a block of text (e.g. lyrics, poetry, or a story) into the input area.
2. Choose the n-gram size to control how closely the generated text follows the original.
3. Set the length of the output text.
4. Click **Generate** to create new text inspired by your input.

The more text you input, the better and more coherent the results!
""")

# Function to create Markov chain
@st.cache_data(show_spinner=False)
def generate_markov_chain(text: str, n: int = 2):
    words = text.split()
    chains = {}
    for i in range(len(words) - n):
        pair = tuple(words[i:i + n])
        next_word = words[i + n]
        chains.setdefault(pair, []).append(next_word)
    return chains

# Function to generate text from Markov chain
def generate_text(chains: dict, n: int = 2, length: int = 50) -> str:
    if not chains:
        return "⚠️ Error: Not enough input text. Please enter a larger block of text."
    
    pair = random.choice(list(chains.keys()))
    result = list(pair)

    for _ in range(length):
        next_words = chains.get(pair)
        if not next_words:
            break
        next_word = random.choice(next_words)
        result.append(next_word)
        pair = tuple(result[-n:])

    return " ".join(result)

# streamlit ui
st.subheader("📝 Input Your Text")
text_input = st.text_area("Paste your lyrics or text here:")

st.subheader("⚙️ Generation Settings")
col1, col2 = st.columns(2)

with col1:
    n = st.slider("N-gram size (context length)", min_value=1, max_value=5, value=2)
with col2:
    length = st.slider("Length of generated text (words)", min_value=10, max_value=200, value=50)

# Button to Gnerate Button
if st.button("🚀 Generate Text"):
    if not text_input or len(text_input.split()) <= n:
        st.warning(f"⚠️ Please enter more text (at least {n + 1} words) for meaningful output.")
    else:
        chains = generate_markov_chain(text_input.strip(), n)
        output = generate_text(chains, n, length)

        st.subheader("🧠 Generated Text Output")
        st.write(output)
else:
    st.info("👆 Enter text and adjust settings, then click **Generate Text** to see results.")

# footer
st.markdown("---")
st.caption('Developed with ❤️ using Python and Streamlit by Muhammad Yousaf | Powered by the <a href="https://myousaf-codes.vercel.app" target="_blank">MYousaf-Codes</a>', unsafe_allow_html=True)
