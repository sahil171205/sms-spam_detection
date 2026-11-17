
import streamlit as st

st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩",
    layout="wide"
)

st.title("📩 SMS Spam Detection")
st.write("Machine Learning Based SMS Spam Detection System")

message = st.text_area("Enter your SMS message:")

if st.button("Check SMS"):
    if message.strip():
        st.info("Message received successfully!")
    else:
        st.warning("Please enter an SMS message.")
