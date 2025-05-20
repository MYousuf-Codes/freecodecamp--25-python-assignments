import streamlit as st

st.set_page_config(page_title="Binary Search", layout="centered")
st.title("🔍 Binary Search Visualizer")

# Input: Sorted array
arr_input = st.text_input("Enter a **sorted list of integers** (comma-separated):", "1,2,3,4,5")

try:
    arr = [int(x.strip()) for x in arr_input.split(",") if x.strip()]
    arr.sort()  # Ensure the list is sorted just in case
except ValueError:
    st.error("Please enter only valid integers separated by commas.")
    st.stop()

# Input: Target value
target = st.number_input("Enter the number to search for:", step=1, format="%d")

# Binary Search Function
def binary_search(arr: list[int], target: int) -> int:
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Search Button
if st.button("🔎 Search"):
    result = binary_search(arr, target)
    if result != -1:
        st.success(f"✅ Element {target} found at **index {result}**.")
    else:
        st.error(f"❌ Element {target} not found in the list.")


# footer
st.markdown("---")
st.caption('Developed with ❤️ using Python and Streamlit by Muhammad Yousaf | Powered by the <a href="https://myousaf-codes.vercel.app" target="_blank">MYousaf-Codes</a>', unsafe_allow_html=True)
