import streamlit as st
import google.generativeai as genai
import PyPDF2

def retrieve_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        st.error(f"Error occurred while extracting text from PDF: {e}")
        return None

# Main function to orchestrate the process
def main():
    try:
        # PDF Path
        pdf_path = r"C:\Users\justin\Downloads\rag application\api_key\leave_no_context_behind.pdf"

        # Model Name
        model_name = "gemini-1.5-pro-latest"

        # Read API key from file
        with open(r"C:\Users\justin\Downloads\rag application\api_key\api.txt",) as f:
            api_key = f.read()

        # Configure the API key
        genai.configure(api_key=api_key)

        # Create Streamlit UI
        st.title("RAG System📃")
        st.subheader("Enhanced AI Contextual Question Answering System: Built on 'Leave No Context Behind' Paper")

        # User input: Question
        question = st.text_input("Ask your question")

        if st.button("Generate Response"):
            if question:
                # Retrieve text
                text = retrieve_text_from_pdf(pdf_path)

                if text:
                    # Concatenate PDF text with question prompt
                    context = text + "\n\n" + question

                    # Initialize the generative model
                    ai = genai.GenerativeModel(model_name=model_name)

                    # Generate response
                    response = ai.generate_content(context)  

                    # Display results
                    st.subheader("Question:")
                    st.write(question)
                    st.subheader("Answer:")
                    st.write(response.text)
                else:
                    st.warning("Failed to retrieve text from PDF.")
            else:
                st.warning("Please enter your question.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()