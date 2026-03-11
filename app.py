import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("Talking Rabbitt 🐰")
st.write("Talk to your business data. Upload a CSV and ask questions.")

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.subheader("Dataset Preview")
        st.dataframe(df)

        question = st.text_input("Ask a question about your data")

        if question:
            prompt = f"""
            You are a business data analyst.

            Here is the dataset:
            {df.head(50).to_string()}

            Question: {question}

            Provide a short clear answer.
            """

            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            st.subheader("AI Answer")
            st.write(response.text)

            if "region" in df.columns and "revenue" in df.columns:
                st.subheader("Revenue by Region")

                chart_data = df.groupby("region")["revenue"].sum()

                fig, ax = plt.subplots()
                chart_data.plot(kind="bar", ax=ax)

                ax.set_xlabel("Region")
                ax.set_ylabel("Revenue")
                ax.set_title("Revenue by Region")

                st.pyplot(fig)

    except Exception as e:
        st.error("Error reading the file or processing data.")
        st.exception(e)
