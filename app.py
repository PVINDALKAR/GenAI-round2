import streamlit as st
from deep_translator import GoogleTranslator
import PyPDF2

# --- Page Config ---
st.set_page_config(
    page_title="Med-Translate AI", 
    page_icon="⚕️", 
    layout="wide"
)

# --- Custom CSS for Design ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
    }
    .report-card {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- Header Section ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063176.png", width=80)
with col2:
    st.title("Med-Translate AI Dashboard")
    st.write("Professional Medical Report Analysis & Translation")

st.divider()

# --- Sidebar Design ---
st.sidebar.header("⚙️ Settings")
languages = {
    "Hindi": "hi", "Marathi": "mr", "Gujarati": "gu", 
    "Bengali": "bn", "Tamil": "ta", "Telugu": "te"
}
selected_lang = st.sidebar.selectbox("Choose Language:", list(languages.keys()))
st.sidebar.info("Tips: For better results, ensure the PDF is not a scanned photo.")

# --- Main Layout ---
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("📁 Input Section")
    uploaded_file = st.file_uploader("Upload Medical PDF", type="pdf")
    
    manual_text = st.text_area("Or Paste Report Text Here:", height=250)

with right_col:
    st.subheader("🔍 Translation Result")
    result_placeholder = st.empty()
    result_placeholder.info("Translation yahan dikhayi degi...")

# --- Logic ---
report_content = ""

if uploaded_file:
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text = page.extract_text()
        if text:
            report_content += text + "\n"
elif manual_text:
    report_content = manual_text

if st.button("🚀 Start Translation"):
    if report_content.strip():
        with st.spinner('Translating medical terms...'):
            try:
                # Limit text to 4500 chars for API safety
                translator = GoogleTranslator(source='auto', target=languages[selected_lang])
                translated_text = translator.translate(report_content[:4500])
                
                with right_col:
                    result_placeholder.success("Translation Complete!")
                    st.markdown(f"""
                    <div class="report-card">
                        <h4>Translated Report ({selected_lang})</h4>
                        <p style='color: #333;'>{translated_text}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.download_button(
                        label="📥 Download as TXT",
                        data=translated_text,
                        file_name="translated_report.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please upload a file or enter text first!")

# --- Footer ---
st.markdown("---")
st.caption("⚠️ Disclaimer: This is an AI-generated translation. Always consult a certified medical professional for diagnosis.")