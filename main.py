import streamlit as st
from streamlit_ace import st_ace
import subprocess

# Page config
st.set_page_config(page_title="MegaEdit", page_icon="💾", layout="wide")
st.title(" MegaEdit")

# Sidebar settings
with st.sidebar:
    theme = st.selectbox("🎨 Theme", ["monokai", "github", "solarized_dark", "solarized_light", "dracula"])
    font_size = st.slider("🔠 Font Size", 12, 24, 14)
    show_gutter = st.checkbox("📏 Show Line Numbers", value=True)
    default_language = st.selectbox("💬 Language", ["python", "javascript", "c", "cpp", "h", "hpp", "hp", "md"], index=0)
    uploaded_file = st.file_uploader("📂 Upload Code File", type=["py", "js", "c", "txt", "cpp", "h", "hpp", "md"])

# Session state: files = {filename: {code, language}}
if "files" not in st.session_state:
    st.session_state.files = {
        "main.py": {"code": "", "language": "python"}
    }

# File upload → load into new tab
if uploaded_file is not None:
    filename = uploaded_file.name
    content = uploaded_file.read().decode("utf-8")
    lang_map = {"py": "python", "js": "javascript", "c": "c", "cpp": "c", "hpp": "c", "h": "c", "md": "javascript", "txt": "javascript"}
    ext = filename.split(".")[-1].lower()
    lang = lang_map.get(ext, default_language)
    st.session_state.files[filename] = {"code": content, "language": lang}
    st.success(f"✅ Uploaded and added as '{filename}'")

# ➕ Add new file
with st.expander("➕ Add New File"):
    new_filename = st.text_input("File name (with extension)", placeholder="e.g. utils.py")
    if st.button("➕ Create File"):
        if new_filename and new_filename not in st.session_state.files:
            ext = new_filename.split(".")[-1].lower()
            lang_map = {"py": "python", "js": "javascript", "c": "c", "cpp": "c", "hpp": "c", "h": "c", "md": "javascript", "txt": "javascript"}
            lang = lang_map.get(ext, default_language)
            st.session_state.files[new_filename] = {"code": "", "language": lang}
            st.success(f"✅ Created new file: {new_filename}")
        elif new_filename in st.session_state.files:
            st.warning("⚠️ File already exists!")

# Show file tabs
file_tabs = list(st.session_state.files.keys())
active_file = st.selectbox("📁 Select File to Edit", file_tabs)

# Load code & language
current_data = st.session_state.files[active_file]
code = st_ace(
    value=current_data["code"],
    language=current_data["language"],
    theme=theme,
    font_size=font_size,
    show_gutter=show_gutter,
    auto_update=True,
    key=f"editor_{active_file}"
)

# Update state
if code is not None:
    st.session_state.files[active_file]["code"] = code

# Run only if Python and main.py
if active_file.endswith(".py") and st.session_state.files[active_file]["language"] == "python":
    if active_file == "main.py":
        st.subheader("▶️ Run main.py")
        if st.button("Run main.py"):
            try:
                with open("temp_main.py", "w") as f:
                    f.write(code)
                result = subprocess.run(["python", "temp_main.py"], capture_output=True, text=True)
                st.subheader("📤 Output:")
                st.text(result.stdout)
                if result.stderr:
                    st.error(result.stderr)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("💡 Only `main.py` can be run.")

# Download file
st.subheader("💾 Download Current File")
if code:
    st.download_button(
        label=f"💾 Download {active_file}",
        data=code,
        file_name=active_file,
        mime="text/plain"
    )
else:
    st.info("Start typing code or upload a file to enable download.")
