import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

genai.configure(api_key="AIzaSyAJYVU0NeEyrujZU1k2lnWlHCR8hnZa55g")

st.title("Talking Rabbitt - Conversational Analytics")

file = st.file_uploader("Upload Sales CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("Dataset Preview")
    st.write(df)

    question = st.text_input("Ask a question about the data")

    if question:
        prompt = f"""
        You are a data analyst.

        Dataset:
        {df.head(50)}

        Question:
        {question}

        Answer clearly in one sentence.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        st.subheader("AI Answer")
        st.write(response.text)

        if "revenue" in df.columns and "region" in df.columns:
            st.subheader("Revenue by Region")

            chart = df.groupby("region")["revenue"].sum()

            chart.plot(kind="bar")

            st.pyplot(plt)