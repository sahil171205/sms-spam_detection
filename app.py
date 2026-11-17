
import streamlit as st
import streamlit.components.v1 as components
import pickle
import re
import html

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="📩",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background-color: #07111f;
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stButton > button {
    background: #0878d1;
    color: white;
    border-radius: 10px;
    border: 1px solid #00aaff;
    padding: 10px 20px;
    font-weight: bold;
}

.stButton > button:hover {
    background: #00aaff;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #101d30;
}

[data-testid="stMetric"] {
    background-color: #101d30;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #234568;
}

.stTextArea textarea {
    background-color: #101d30 !important;
    color: white !important;
    border: 1px solid #0878d1;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD TRAINED MODEL ----------------
@st.cache_resource
def load_model():
    with open("spam_model.pkl", "rb") as file:
        data = pickle.load(file)

    return data["model"], data["vectorizer"]


try:
    model, vectorizer = load_model()

except Exception as e:
    st.error("ML Model Loading Failed!")
    st.warning(
        "Check whether spam_model.pkl exists in GitHub."
    )
    st.code(str(e))
    st.stop()


# ---------------- SPAM RULES ----------------

# ---------------- SPAM RULES ----------------
def check_suspicious_sms(message):

    patterns = [
        # Lottery Scams
        r"\bwon\s+(a\s+)?lottery\b",
        r"\blottery\s+(winner|prize|ticket)\b",
        r"\byou\s+have\s+won\b",
        r"\bclaim\s+(your\s+)?(free\s+)?(prize|reward|cash)\b",
        r"\bcash\s+prize\b",
        r"\bjackpot\b",

        # Bank and KYC Fraud
        r"\bbank\s+account\s+will\s+be\s+blocked\b",
        r"\bverify\s+your\s+kyc\b",
        r"\bupdate\s+your\s+kyc\s+immediately\b",
        r"\baccount\s+(will\s+be\s+)?(blocked|suspended)\b",
        r"\bkyc\s+(expired|pending|failed)\b",
        r"\bverify\s+your\s+bank\s+account\b",

        # OTP and Password Scams
        r"\bshare\s+your\s+otp\b",
        r"\bsend\s+(me\s+)?your\s+otp\b",
        r"\bshare\s+your\s+password\b",

        # Suspicious Prize Messages
        r"\bfree\s+entry\b",
        r"\bclick\s+here\s+to\s+claim\b",
        r"\bselected\s+as\s+(a\s+)?(lucky\s+)?winner\b"
    ]

    return any(
        re.search(pattern, message, re.IGNORECASE)
        for pattern in patterns
    )

# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "result" not in st.session_state:
    st.session_state.result = None

if "message" not in st.session_state:
    st.session_state.message = ""

if "spam_probability" not in st.session_state:
    st.session_state.spam_probability = 0.0

if "rule_detected" not in st.session_state:
    st.session_state.rule_detected = False


# ---------------- SIDEBAR ----------------
st.sidebar.title("🛡️ CYBER SECURITY")
st.sidebar.caption("AI SMS Protection System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Detection History",
        "About Project"
    ]
)

st.sidebar.markdown("---")
st.sidebar.success("ML Model: LOADED")
st.sidebar.info("System Status: ACTIVE")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("📩 SMS SPAM DETECTION")
    st.write("Machine Learning Based SMS Security System")

    total = len(st.session_state.history)

    spam_count = sum(
        1 for x in st.session_state.history
        if x["result"] == "spam"
    )

    normal_count = sum(
        1 for x in st.session_state.history
        if x["result"] == "normal"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Scans", total)
    c2.metric("Spam Messages", spam_count)
    c3.metric("Normal Messages", normal_count)

    st.markdown("---")
    st.subheader("🔍 SMS Security Scanner")

    message = st.text_area(
        "Enter your SMS:",
        value=st.session_state.message,
        height=130,
        placeholder="Enter or paste your SMS here..."
    )

    if st.button(
        "🚀 SCAN MESSAGE",
        use_container_width=True
    ):

        if message.strip():

            # TF-IDF Transformation
            msg_vector = vectorizer.transform(
                [message]
            )

            # ML Prediction
            prediction = str(
                model.predict(msg_vector)[0]
            ).lower().strip()

            # Model Probability
            probabilities = model.predict_proba(
                msg_vector
            )[0]

            spam_index = list(
                model.classes_
            ).index("spam")

            spam_probability = float(
                probabilities[spam_index]
            ) * 100

            # Additional Spam Rules
            suspicious = check_suspicious_sms(
                message
            )

            if prediction == "spam" or suspicious:
                result = "spam"
            else:
                result = "normal"

            # Save Session Result
            st.session_state.result = result
            st.session_state.message = message
            st.session_state.spam_probability = spam_probability
            st.session_state.rule_detected = suspicious

            st.session_state.history.insert(
                0,
                {
                    "message": message,
                    "result": result,
                    "spam_probability": spam_probability
                }
            )

        else:
            st.warning("Please enter an SMS first.")


    # ---------------- RESULT ----------------
    if st.session_state.result is not None:

        result = st.session_state.result

        if result == "spam":

            st.markdown("""
            <div style="
                background:#421414;
                border:2px solid #ff3030;
                padding:25px;
                border-radius:15px;
                text-align:center;
            ">
                <h1 style="color:#ff3030 !important;">
                    ⚠️ SPAM MESSAGE DETECTED
                </h1>

                <h3 style="color:white !important;">
                    SUSPICIOUS MESSAGE - BE CAREFUL
                </h3>

                <div style="
                    width:35px;
                    height:35px;
                    border-radius:50%;
                    background:#ff2020;
                    margin:20px auto;
                    box-shadow:0 0 30px red;
                    animation:redblink 1s infinite;
                "></div>

                <h3 style="color:#ff3030 !important;">
                    🔴 RED ALERT
                </h3>
            </div>

            <style>
            @keyframes redblink {
                0%,100% {
                    opacity:1;
                    box-shadow:0 0 30px red;
                }
                50% {
                    opacity:0.2;
                    box-shadow:0 0 5px red;
                }
            }
            </style>
            """, unsafe_allow_html=True)

            st.error(
                "⚠️ Warning: This SMS may be fraudulent."
            )

            if st.button("🔊 PLAY ALARM"):
                components.html("""
                <audio controls autoplay>
                    <source
                    src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
                    type="audio/ogg">
                </audio>
                """, height=65)

        # ---------------- NORMAL RESULT ----------------
        else:

            st.markdown("""
            <div style="
                background:#103528;
                border:2px solid #00ff88;
                padding:25px;
                border-radius:15px;
                text-align:center;
            ">
                <h1 style="color:#00ff88 !important;">
                    ✅ NORMAL MESSAGE
                </h1>

                <h3 style="color:white !important;">
                    NO SPAM DETECTED
                </h3>

                <div style="
                    width:35px;
                    height:35px;
                    border-radius:50%;
                    background:#00ff88;
                    margin:20px auto;
                    box-shadow:0 0 30px #00ff88;
                    animation:greenblink 1s infinite;
                "></div>

                <h3 style="color:#00ff88 !important;">
                    🟢 GREEN SAFE
                </h3>
            </div>

            <style>
            @keyframes greenblink {
                0%,100% {
                    opacity:1;
                    box-shadow:0 0 30px #00ff88;
                }
                50% {
                    opacity:0.25;
                    box-shadow:0 0 5px #00ff88;
                }
            }
            </style>
            """, unsafe_allow_html=True)

            st.success(
                "✅ This message is classified as NORMAL."
            )

        # ---------------- PROBABILITY ----------------
        st.markdown("---")
        st.subheader("📊 ML Analysis")

        probability = st.session_state.spam_probability

        st.metric(
            "ML Spam Probability",
            f"{probability:.2f}%"
        )

        st.progress(
            min(max(probability / 100, 0.0), 1.0)
        )

        if st.session_state.rule_detected:
            st.info(
                "Suspicious keyword pattern detected. "
                "The final result also uses rule-based detection."
            )

        st.caption(
            "Probability is an ML estimate, not a safety guarantee."
        )


# ---------------- DETECTION HISTORY ----------------
elif page == "Detection History":

    st.title("📋 DETECTION HISTORY")

    if st.session_state.history:

        for i, item in enumerate(
            st.session_state.history,
            start=1
        ):

            st.markdown(
                f"**Scan {i}:**"
            )

            st.text(item["message"])

            if item["result"] == "spam":
                st.error("🔴 SPAM MESSAGE")
            else:
                st.success("🟢 NORMAL MESSAGE")

            st.markdown("---")

        if st.button("🗑️ CLEAR HISTORY"):

            st.session_state.history = []
            st.session_state.result = None
            st.session_state.message = ""
            st.session_state.spam_probability = 0.0
            st.session_state.rule_detected = False

            st.rerun()

    else:
        st.info("No detection history available.")


# ---------------- ABOUT PROJECT ----------------
elif page == "About Project":

    st.title("ℹ️ ABOUT PROJECT")

    st.markdown("""
    ### SMS Spam Detection System

    This project uses Machine Learning to identify
    spam and normal SMS messages.

    ### Technologies Used

    - Python
    - Streamlit
    - Scikit-learn
    - TF-IDF Vectorizer
    - Multinomial Naive Bayes

    ### Features

    - SMS Spam Detection
    - Trained Machine Learning Model
    - Lottery Scam Detection Rules
    - Red Blinking Spam Alert
    - Green Blinking Normal Indicator
    - Alarm Sound Button
    - Spam Probability
    - Detection History

    ### Project Objective

    To classify SMS messages and help identify
    suspicious or unwanted messages.
    """)


# ---------------- FOOTER ----------------
st.markdown("---")

st.caption(
    "🛡️ SMS Spam Detection | AI Cyber Security Project"
)
