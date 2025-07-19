import streamlit as st
from streamlit_ace import st_ace
import subprocess

# Page configuration
st.set_page_config(page_title="Code Editor", page_icon="💾", layout="wide")

# Title
st.title("MegaEdit")
st.write("Write your code below. You can run Python code or save any code.")

# Sidebar settings
with st.sidebar:
    theme = st.selectbox("🎨 Editor Theme", ["monokai", "github", "solarized_dark", "solarized_light", "dracula"])
    font_size = st.slider("🔠 Font Size", 12, 24, 14)
    show_gutter = st.checkbox("📏 Show Line Numbers", value=True)
    language = st.selectbox("💬 Language", ["python", "javascript", "c"], index=0)

# Code editor
code = st_ace(
    language=language,
    theme=theme,
    font_size=font_size,
    show_gutter=show_gutter,
    auto_update=True,
    key="editor"
)

# Run section (Python only)
if language == "python":
    st.subheader("▶️ Run Code")
    if st.button("Run Code"):
        try:
            with open("temp_code.py", "w") as f:
                f.write(code)

            result = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True)

            st.subheader("📤 Output:")
            st.text(result.stdout)
            if result.stderr:
                st.error(result.stderr)
        except Exception as e:
            st.error(f"Error: {e}")

# Save code as file
st.subheader("💾 Save Code")
if code:
    file_extension = {
        "python": "py",
        "javascript": "js",
        "c": "c"
    }.get(language, "txt")

    filename = f"my_code.{file_extension}"
    st.download_button(
        label="💾 Download Code File",
        data=code,
        file_name=filename,
        mime="text/plain"
    )
else:
    st.info("⏳ Start typing code to enable download.")

# Console placeholder
st.subheader("🧾 Console (placeholder)")
st.text_area("Console Output (for future features)", height=200, key="console_output", disabled=True)
