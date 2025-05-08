import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

# Custom CSS for styling
def apply_custom_styles():
    st.markdown("""
        <style>
            .main {
                background-color: #f0f4f8;
            }
            .logo-fixed {
                position: fixed;
                top: 0.5rem;
                left: 1rem;
                font-size: 24px;
                font-weight: 800;
                color: #1f77b4;
                z-index: 9999;
            }
            .stButton>button {
                background-color: #1f77b4;
                color: white;
                border: None;
                border-radius: 5px;
                padding: 0.5em 1em;
            }
            .stTextInput>div>div>input {
                background-color: #ffffff;
                color: #000;
            }
            .stSpinner {
                color: #1f77b4;
            }
        </style>
        <div class="logo-fixed">📘 Maxi Production</div>
    """, unsafe_allow_html=True)


def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.markdown(f"**🧑 User:** {message.content}")
        else:
            st.markdown(f"**🤖 Reply:** {message.content}")

def main():
    st.set_page_config(page_title="Information Retrieval", page_icon="📄", layout="wide")
    apply_custom_styles()

    st.header("Information Retrieval System")
    st.markdown("---")

    user_question = st.text_input("💬 Ask a Question from the PDF Files", placeholder="Type your question here...")

    # Session state init
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        user_input(user_question)

    # Sidebar
    with st.sidebar:
        st.title("📂 Menu")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True, type=["pdf"])
        if st.button("✅ Submit & Process"):
            with st.spinner("🔄 Processing..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("✅ Done")

if __name__ == "__main__":
    main()
