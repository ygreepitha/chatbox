import streamlit as st
import requests

st.title("AI Chat Application")
st.write("Upload your PDF and ask questions based on its content.")


uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:

    files = {'file': uploaded_file}

    response = requests.post("http://localhost:8000/chat/api/upload/", files=files)


    if response.status_code == 201:
        st.success("PDF uploaded successfully!")
    else:

        if response.headers.get('Content-Type') == 'application/json':
            response_json = response.json()
            st.error("Upload Error: {}".format(response_json.get("error", "An unknown error occurred.")))
        else:
            st.error("Received an invalid response from the server: {}".format(response.text))


query = st.text_input("Enter your question:")
if st.button("Get Answer"):

    response = requests.post("http://localhost:8000/chat/api/chat/", json={"query": query})

    if response.headers.get('Content-Type') == 'application/json':
        response_json = response.json()
        
        if response.status_code == 200:
            st.write("Answer:", response_json.get("answer", "No answer found."))
        else:
            st.error("Chat Error: {}".format(response_json.get("error", "An unknown error occurred.")))
    else:
        st.error("Error: Received an invalid response from the server: {}".format(response.text))
