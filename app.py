import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

st.set_page_config(page_title="Talking Rabbitt", layout="wide")

st.title("Talking Rabbitt 🐰")
st.write("Upload your sales data and ask questions about your business.")

api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

uploaded_file = st.file_uploader("Upload Sales CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    question = st.text_input("Ask a question about the data")

    if question:
        prompt = f"""
        You are a business data analyst.

        Dataset:
        {df.head(50).to_string()}

        Question: {question}

        Answer clearly in one sentence.
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        st.subheader("AI Answer")
        st.write(response.text)

        if "region" in df.columns and "revenue" in df.columns:
            st.subheader("Revenue by Region")

            chart_data = df.groupby("region")["revenue"].sum().reset_index()

            fig = px.bar(
                chart_data,
                x="region",
                y="revenue",
                title="Revenue by Region"
            )

            st.plotly_chart(fig, use_container_width=True)
