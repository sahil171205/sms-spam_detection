
import streamlit as st
import pickle
import re
import html

# ----------------------------------
# PAGE CONFIGURATION
# ----------------------------------

st.set_page_config(
    page_title="AI SMS Spam Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------
# LOAD TRAINED MODEL
# ----------------------------------

@st.cache_resource
def load_model():
    with open("spam_model.pkl", "rb") as file:
        data = pickle.load(file)

    return data["model"], data["vectorizer"]


try:
    model, vectorizer = load_model()
except Exception as e:
    st.error("Unable to load trained ML model.")
    st.exception(e)
    st.stop()


# ----------------------------------
# PROFESSIONAL WHITE + BLUE CSS
# ----------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #f5f8fc;
    color: #172b4d;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #172b4d !important;
}

[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e4eaf3;
}

[data-testid="stSidebar"] * {
    color: #172b4d;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e4eaf3;
    border-radius: 14px;
    padding: 18px;
}

[data-testid="stMetricValue"] {
    color: #1463df;
}

.stButton > button {
    background: #1463df;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 600;
    padding: 12px 20px;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #0b4db5;
    color: white;
    border: none;
}

.stTextArea textarea {
    background-color: #ffffff !important;
    color: #172b4d !important;
    border: 1px solid #d8e2f0 !important;
    border-radius: 12px !important;
}

.hero {
    background: linear-gradient(
        120deg,
        #1463df,
        #4396f5
    );
    border-radius: 20px;
    padding: 35px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white !important;
    font-size: 34px;
    margin-bottom: 10px;
}

.hero p {
    color: #edf5ff;
    font-size: 16px;
}

.info-card {
    background: #ffffff;
    border: 1px solid #e4eaf3;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
    box-shadow: 0 3px 12px rgba(30,60,100,0.04);
}

.info-card h3 {
    margin-top: 0;
}

.result-spam {
    background: #fff1f2;
    border: 1px solid #fecdd3;
    border-left: 5px solid #e11d48;
    border-radius: 14px;
    padding: 24px;
    color: #9f1239;
}

.result-normal {
    background: #ecfdf5;
    border: 1px solid #a7f3d0;
    border-left: 5px solid #059669;
    border-radius: 14px;
    padding: 24px;
    color: #065f46;
}

.result-spam h2 {
    color: #be123c !important;
}

.result-normal h2 {
    color: #047857 !important;
}

.result-spam p {
    color: #9f1239;
}

.result-normal p {
    color: #065f46;
}

.footer {
    text-align: center;
    color: #64748b;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ----------------------------------
# SESSION STATE
# ----------------------------------

if "total_scans" not in st.session_state:
    st.session_state.total_scans = 0

if "spam_scans" not in st.session_state:
    st.session_state.spam_scans = 0

if "normal_scans" not in st.session_state:
    st.session_state.normal_scans = 0

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ----------------------------------
# SIDEBAR
# ----------------------------------

with st.sidebar:

    st.title("🛡️ SMS Guardian AI")

    st.caption("Intelligent Message Security")

    st.divider()

    st.markdown("### Navigation")

    page = st.radio(
        "Select Page",
        [
            "Dashboard",
            "About Project"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### Machine Learning")

    st.write("Model: Multinomial Naive Bayes")
    st.write("Feature Extraction: TF-IDF")
    st.write("Language: Python")
    st.write("Framework: Streamlit")

    st.divider()

    st.success("● ML Model Loaded")


# ----------------------------------
# DASHBOARD
# ----------------------------------

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>🛡️ AI SMS Spam Detector</h1>
        <p>
        Smart SMS Security powered by
        Machine Learning and Natural Language Processing.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Dashboard Statistics

    st.subheader("📊 Dashboard Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Messages Scanned",
            st.session_state.total_scans
        )

    with col2:
        st.metric(
            "Spam Detected",
            st.session_state.spam_scans
        )

    with col3:
        st.metric(
            "Normal Messages",
            st.session_state.normal_scans
        )

    st.caption(
        "Statistics are for your current session only."
    )

    st.divider()

    # Message Input

    st.subheader("📩 SMS Message Analysis")

    st.markdown("""
    <div class="info-card">
        <h3>Analyze Your Message</h3>
        <p>
        Enter an SMS message below to check
        whether it is Spam or Normal.
        </p>
    </div>
    """, unsafe_allow_html=True)

    message = st.text_area(
        "Enter SMS Message",
        placeholder="Type or paste your SMS here...",
        height=160
    )

    analyze = st.button(
        "🔍 Analyze Message",
        use_container_width=True
    )

    # ----------------------------------
    # ML PREDICTION
    # ----------------------------------

    if analyze:

        if not message.strip():

            st.warning(
                "Please enter an SMS message."
            )

        else:

            message_vector = vectorizer.transform(
                [message]
            )

            prediction = model.predict(
                message_vector
            )[0]

            probabilities = model.predict_proba(
                message_vector
            )[0]

            spam_index = list(
                model.classes_
            ).index("spam")

            spam_probability = float(
                probabilities[spam_index]
            ) * 100

            confidence = (
                spam_probability
                if prediction == "spam"
                else 100 - spam_probability
            )

            # Update Statistics

            st.session_state.total_scans += 1

            if prediction == "spam":
                st.session_state.spam_scans += 1
            else:
                st.session_state.normal_scans += 1

            st.session_state.last_result = {
                "message": message,
                "prediction": prediction,
                "spam_probability": spam_probability,
                "confidence": confidence
            }

    # ----------------------------------
    # DISPLAY RESULT
    # ----------------------------------

    result = st.session_state.last_result

    if result is not None:

        st.divider()

        st.subheader("📋 Analysis Result")

        prediction = result["prediction"]

        if prediction == "spam":

            st.markdown("""
            <div class="result-spam">
                <h2>🚨 SPAM DETECTED</h2>
                <p>
                This message may contain
                suspicious or unwanted content.
                </p>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="result-normal">
                <h2>✅ NORMAL MESSAGE</h2>
                <p>
                The model classified this
                message as normal.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.write("")

        result_col1, result_col2 = st.columns(2)

        with result_col1:

            st.metric(
                "Spam Probability",
                f"{result['spam_probability']:.2f}%"
            )

        with result_col2:

            st.metric(
                "Model Confidence",
                f"{result['confidence']:.2f}%"
            )

        st.subheader("📈 Spam Probability")

        st.progress(
            min(
                max(
                    result["spam_probability"] / 100,
                    0.0
                ),
                1.0
            )
        )

        st.caption(
            "Probabilities are model estimates, "
            "not calibrated guarantees."
        )

        # Message Statistics

        st.subheader("📊 Message Statistics")

        analyzed_message = result["message"]

        word_count = len(
            analyzed_message.split()
        )

        char_count = len(analyzed_message)

        url_count = len(
            re.findall(
                r"https?://\\S+|www\\.\\S+",
                analyzed_message
            )
        )

        stat1, stat2, stat3 = st.columns(3)

        stat1.metric("Words", word_count)
        stat2.metric("Characters", char_count)
        stat3.metric("URLs", url_count)

        st.markdown("### Analyzed Message")

        st.info(analyzed_message)

        if prediction == "spam":
            st.warning(
                "Avoid clicking suspicious links "
                "or sharing personal information."
            )

        else:
            st.info(
                "A normal classification does not "
                "guarantee that a message is safe."
            )


# ----------------------------------
# ABOUT PROJECT
# ----------------------------------

elif page == "About Project":

    st.title("📘 About SMS Spam Detection")

    st.markdown("""
    ### Project Overview

    SMS Spam Detection is a Machine Learning
    based project designed to classify text
    messages as Spam or Normal.

    ### Technologies Used

    - Python
    - Streamlit
    - Pandas
    - Scikit-learn
    - TF-IDF Vectorizer
    - Multinomial Naive Bayes

    ### Working Process

    1. User enters an SMS message.
    2. Text is converted into TF-IDF features.
    3. Trained ML model analyzes the message.
    4. Model predicts Spam or Normal.
    5. Website displays prediction and probability.

    ### Project Domain

    - Machine Learning
    - Natural Language Processing
    - Cybersecurity

    ### Dataset

    UCI SMS Spam Collection Dataset

    ### Objective

    To develop an intelligent SMS classification
    system using Machine Learning techniques.
    """)


# ----------------------------------
# FOOTER
# ----------------------------------

st.divider()

st.markdown("""
<div class="footer">
    AI SMS Spam Detector | Professional ML Dashboard
    <br>
    Built with Python, Scikit-learn and Streamlit
</div>
""", unsafe_allow_html=True)
