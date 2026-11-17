
import streamlit as st
import pickle

# Page Configuration
st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩",
    layout="wide"
)

# Load Trained ML Model
@st.cache_resource
def load_model():
    with open("spam_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data["model"], data["vectorizer"]

model, vectorizer = load_model()

# Website Title
st.title("📩 SMS Spam Detection")
st.subheader("Machine Learning Based SMS Classification")
st.write("Detect whether your SMS is Spam or Normal.")

# SMS Input
message = st.text_area(
    "Enter your SMS Message:",
    placeholder="Type or paste your SMS here...",
    height=150
)

# Detection Button
if st.button("🔍 Check SMS", use_container_width=True):

    if not message.strip():
        st.warning("Please enter an SMS message.")

    else:
        # Convert SMS into TF-IDF Features
        message_vector = vectorizer.transform([message])

        # Predict using ML Model
        prediction = model.predict(message_vector)[0]

        # Display Result
        if prediction == "spam":
            st.error("🚨 SPAM MESSAGE DETECTED!")
            st.warning("Be careful! This message may be suspicious.")
        else:
            st.success("✅ NORMAL MESSAGE")
            st.info("This message is classified as normal.")

# Footer
st.markdown("---")
st.caption("SMS Spam Detection | Machine Learning Project")
