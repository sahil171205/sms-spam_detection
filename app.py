
import streamlit as st
import pickle
import html

st.set_page_config(
    page_title="AI SMS Spam Detector",
    page_icon="🛡️",
    layout="wide"
)

# Load ML Model
@st.cache_resource
def load_model():
    with open("spam_model.pkl", "rb") as file:
        data = pickle.load(file)
    return data["model"], data["vectorizer"]

model, vectorizer = load_model()

# Professional Dark Theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #050b18, #101f35);
    color: #ffffff;
}

h1, h2, h3, p, label {
    color: #ffffff !important;
}

.block-container {
    max-width: 1050px;
    padding-top: 3rem;
}

.stButton > button {
    background: linear-gradient(90deg, #007bff, #00c6ff);
    color: white;
    border: none;
    border-radius: 12px;
    font-weight: bold;
    padding: 12px;
}

.stButton > button:hover {
    background: #0056b3;
    color: white;
}

div[data-testid="stTextArea"] textarea {
    background-color: #101c30;
    color: white;
    border: 1px solid #248cff;
    border-radius: 12px;
}

.cyber-card {
    background: #101d31;
    border: 1px solid #253b59;
    border-radius: 15px;
    padding: 25px;
    margin: 15px 0;
}

.spam-result {
    background: #3b101b;
    border: 2px solid #ff354d;
    border-radius: 15px;
    padding: 25px;
    color: white;
}

.ham-result {
    background: #103b2b;
    border: 2px solid #00dd88;
    border-radius: 15px;
    padding: 25px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Header
st.title("🛡️ AI SMS Spam Detector")
st.caption("Machine Learning Powered Message Security")

st.markdown("""
<div class="cyber-card">
    <h3>🔐 Intelligent SMS Security</h3>
    <p>
    Analyze suspicious messages using Machine Learning
    and Natural Language Processing.
    </p>
</div>
""", unsafe_allow_html=True)

# Input
st.subheader("📩 Message Analysis")

message = st.text_area(
    "Enter SMS Message",
    placeholder="Paste your SMS message here...",
    height=160
)

# Detection
if st.button("🔍 ANALYZE MESSAGE", use_container_width=True):

    if not message.strip():
        st.warning("Please enter an SMS message.")

    else:
        message_vector = vectorizer.transform([message])

        prediction = model.predict(message_vector)[0]

        probabilities = model.predict_proba(
            message_vector
        )[0]

        spam_index = list(model.classes_).index("spam")
        spam_probability = probabilities[spam_index] * 100

        if prediction == "spam":
            st.markdown("""
            <div class="spam-result">
                <h2>🚨 SPAM DETECTED</h2>
                <p>This message may be suspicious.</p>
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="ham-result">
                <h2>✅ NORMAL MESSAGE</h2>
                <p>No spam detected by the model.</p>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📊 Spam Probability")

        st.progress(
            min(max(float(spam_probability / 100), 0.0), 1.0)
        )

        st.metric(
            "Estimated Spam Probability",
            f"{spam_probability:.2f}%"
        )

        st.caption(
            "Model estimate only. Not a guarantee of message safety."
        )

st.markdown("---")
st.caption("AI SMS Spam Detector | Machine Learning & Cybersecurity")
