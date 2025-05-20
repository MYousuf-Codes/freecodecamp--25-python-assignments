import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance

st.set_page_config(page_title="Photo Manipulation Tool", layout="wide")
st.title("🖼️ Photo Manipulation Tool")

uploaded_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    original_image = Image.open(uploaded_file)
    
    st.markdown("### 🔍 Zoom Settings")
    zoom_level = st.slider("Zoom Level", 10, 200, 100, step=10)  # Percent scale
    zoom_scale = zoom_level / 100

    def resize_image(img, scale):
        width, height = img.size
        return img.resize((int(width * scale), int(height * scale)))

    resized_original = resize_image(original_image, zoom_scale)
    modified_image = original_image.copy()

    st.markdown("---")
    st.subheader("🎛️ Adjustments")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 📸 Original Image (Zoom Applied)")
        st.image(resized_original, use_container_width=False)

    # this is effects and filters control
    effect = st.selectbox("Choose an Effect", ["None", "Grayscale", "Blur", "Rotate"])
    brightness = st.slider("Brightness", 0.1, 2.0, 1.0, 0.1)
    contrast = st.slider("Contrast", 0.1, 2.0, 1.0, 0.1)

    # here the applying the adjustments
    modified_image = ImageEnhance.Brightness(modified_image).enhance(brightness)
    modified_image = ImageEnhance.Contrast(modified_image).enhance(contrast)

    if effect == "Grayscale":
        modified_image = modified_image.convert("L")
    elif effect == "Blur":
        blur_radius = st.slider("Blur intensity", 0.0, 10.0, 2.0, 0.1)
        modified_image = modified_image.filter(ImageFilter.GaussianBlur(blur_radius))
    elif effect == "Rotate":
        angle = st.slider("Rotation Angle", 0, 360, 90)
        modified_image = modified_image.rotate(angle)

    resized_modified = resize_image(modified_image, zoom_scale)

    with col2:
        st.markdown(f"##### 🖌️ Edited Image (Effect: `{effect}`)")
        st.image(resized_modified, use_container_width=False)

    # Download button
    st.download_button(
        label="📥 Download Modified Image",
        data=modified_image.convert("RGB").tobytes(),
        file_name="edited_image.jpg",
        mime="image/jpeg"
    )

# footer
st.markdown("---")
st.caption('Developed with ❤️ using Python and Streamlit by Muhammad Yousaf | Powered by the <a href="https://myousaf-codes.vercel.app" target="_blank">MYousaf-Codes</a>', unsafe_allow_html=True)
