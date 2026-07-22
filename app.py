import streamlit as st
from config import secret_key_valid
from pdf_reading_file import extract_text
from rag import (
    create_chunks,
    create_vector_store,
    ask_question
)



st.set_page_config(
    page_title="AI Document QA",
    page_icon="📄"
)

st.title("📄 AI Document Question Answering")

secret_key = st.text_input(
    "Enter Your Secret Key",
    type="password"
)


if st.button("Submit"):
        if secret_key == "":
            st.error("Please enter a Secret Key.")
        else:
            api_key = secret_key_valid(secret_key)
            # print(">>"+api_key)
            if api_key:
                st.success("Secret Key is valid. Configuration saved.")

                st.session_state["secret_key"] = secret_key
            else:
                st.error("Invalid Secret Key. Please try again.")

st.header("Upload your Document")


uploaded_file = st.file_uploader(
    "Upload your PDF here",
    type=["pdf"]
)


if uploaded_file:

    if "secret_key" not in st.session_state:
        st.warning(
            "Please submit Secret key first."
        )

    else:

        document_text = extract_text(
            uploaded_file
        )


        chunks = create_chunks(
            document_text
        )


        vector_store = create_vector_store(
            chunks,
            st.session_state["secret_key"]
        )


        st.session_state["vector_store"] = vector_store


        st.success(
            "PDF uploaded successfully. you can ask questions now"
        )
        

st.header("Ask Questions From Document")


question = st.text_input(
    "Enter your question"
)


if st.button("Get Answer"):

    if "vector_store" not in st.session_state:

        st.error(
            "Please upload your PDF first."
        )

    elif question == "":

        st.error(
            "Please enter a question."
        )

    else:

        answer = ask_question(
            st.session_state["vector_store"],
            question,
            st.session_state["secret_key"]
        )


        st.success("Answer:")

        st.markdown(f"""
        <div style="font-size: 24px; font-weight: bold;">{answer}</div>""",
        unsafe_allow_html=True
        )