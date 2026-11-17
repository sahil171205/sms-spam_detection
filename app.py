
import streamlit as st
import streamlit.components.v1 as components
import pickle
import re
import html

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SMS Spam Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: #07111f;
    color: white;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
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
    border: 1px solid #234568;
    border-radius: 12px;
    padding: 18px;
}

.stTextArea textarea {
    background-color: #101d30 !important;
    color: white !important;
    border: 1px solid #0878d1 !important;
    border-radius: 10px !important;
}

.alert-box {
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-top: 15px;
}

.spam-box {
    background: #421414;
    border: 2px solid #ff3030;
}

.normal-box {
    background: #103528;
    border: 2px solid #00ff88;
}

.alert-box h2,
.alert-box h3 {
    margin: 12px 0;
}

.spam-box h2,
.spam-box h3 {
    color: #ff5050 !important;
}

.normal-box h2,
.normal-box h3 {
    color: #00ff88 !important;
}

.alert-light {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    margin: 20px auto;
}

.red-light {
    background: #ff2020;
    animation: redblink 1s infinite;
}

.green-light {
    background: #00ff88;
    animation: greenblink 1s infinite;
}

@keyframes redblink {
    0%, 100% {
        opacity: 1;
        box-shadow: 0 0 30px red;
    }
    50% {
        opacity: 0.2;
        box-shadow: 0 0 5px red;
    }
}

@keyframes greenblink {
    0%, 100% {
        opacity: 1;
        box-shadow: 0 0 30px #00ff88;
    }
    50% {
        opacity: 0.25;
        box-shadow: 0 0 5px #00ff88;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- LOAD ML MODEL ----------------
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
        "Check spam_model.pkl in your GitHub repository."
    )
    st.code(str(e))
    st.stop()


# ---------------- SPAM RULES ----------------
def check_suspicious_sms(message):

    patterns = [
        # Lottery Fraud
        r"\bwon\s+(a\s+)?lottery\b",
        r"\blottery\s+(winner|prize|ticket)\b",
        r"\byou\s+have\s+won\b",
        r"\bclaim\s+(your\s+)?(free\s+)?(prize|reward|cash)\b",
        r"\bcash\s+prize\b",
        r"\bjackpot\b",
        r"\bfree\s+entry\b",
        r"\bclick\s+here\s+to\s+claim\b",
        r"\bselected\s+as\s+(a\s+)?(lucky\s+)?winner\b",

        # Bank / KYC Fraud
        r"\bbank\s+account\s+will\s+be\s+blocked\b",
        r"\bverify\s+your\s+kyc\b",
        r"\bupdate\s+your\s+kyc\s+immediately\b",
        r"\baccount\s+(will\s+be\s+)?(blocked|suspended)\b",
        r"\bkyc\s+(expired|pending|failed)\b",
        r"\bverify\s+your\s+bank\s+account\b",

        
         r"\bwon\b",
        
        r"\byou\s+(have\s+)?won\s+(a\s+)?car\b",



        # OTP / Password Fraud
        r"\bshare\s+your\s+otp\b",
        r"\bsend\s+(me\s+)?your\s+otp\b",
        r"\bshare\s+your\s+password\b",
        r"\bprovide\s+your\s+otp\b",

        # Suspicious Payment Scams
        r"\bpay\s+(a\s+)?(small\s+)?fee\s+to\s+claim\b",
        r"\bclick\s+the\s+link\s+to\s+verify\b",
        r"\bclaim\s+your\s+reward\b"
    ]

    return any(
        re.search(pattern, message, re.IGNORECASE)
        for pattern in patterns
    )


# ---------------- SESSION STATE ----------------
defaults = {
    "history": [],
    "result": None,
    "message": "",
    "spam_probability": 0.0,
    "rule_detected": False,
    "scan_id": 0
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


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
    st.caption("Machine Learning Based SMS Security System")

    total = len(st.session_state.history)

    spam_count = sum(
        item["result"] == "spam"
        for item in st.session_state.history
    )

    normal_count = sum(
        item["result"] == "normal"
        for item in st.session_state.history
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Scans", total)
    col2.metric("Spam Messages", spam_count)
    col3.metric("Normal Messages", normal_count)

    st.divider()

    st.subheader("🔍 SMS Security Scanner")

    message = st.text_area(
        "Enter your SMS:",
        value=st.session_state.message,
        height=140,
        placeholder="Enter or paste your SMS here..."
    )

    if st.button(
        "🚀 SCAN MESSAGE",
        use_container_width=True
    ):

        if not message.strip():
            st.warning("Please enter an SMS first.")

        else:
            # TF-IDF Features
            msg_vector = vectorizer.transform(
                [message]
            )

            # ML Prediction
            prediction = str(
                model.predict(msg_vector)[0]
            ).lower().strip()

            # Probability
            probabilities = model.predict_proba(
                msg_vector
            )[0]

            spam_index = list(
                model.classes_
            ).index("spam")

            spam_probability = float(
                probabilities[spam_index]
            ) * 100

            # Rule-Based Detection
            suspicious = check_suspicious_sms(
                message
            )

            if prediction == "spam" or suspicious:
                result = "spam"
            else:
                result = "normal"

            # Save Results
            st.session_state.result = result
            st.session_state.message = message
            st.session_state.spam_probability = (
                spam_probability
            )
            st.session_state.rule_detected = suspicious

            st.session_state.scan_id += 1

            st.session_state.history.insert(
                0,
                {
                    "message": message,
                    "result": result,
                    "probability": spam_probability
                }
            )

    # ---------------- RESULT DISPLAY ----------------
    if st.session_state.result is not None:

        result = st.session_state.result

        if result == "spam":

            st.markdown("""
            <div class="alert-box spam-box">
                <h2>⚠️ SPAM MESSAGE DETECTED</h2>
                <h3>SUSPICIOUS MESSAGE - BE CAREFUL</h3>
                <div class="alert-light red-light"></div>
                <h3>🔴 RED ALERT</h3>
            </div>
            """, unsafe_allow_html=True)

            st.error(
                "⚠️ Warning: This SMS may be fraudulent."
            )

            # Automatic Alarm Attempt
            # Browser may block autoplay with sound.
            components.html("""
            <audio id="spamAlarm" controls autoplay>
                <source
                    src="https://actions.google.com/sounds/v1/alarms/alarm_clock.ogg"
                    type="audio/ogg">
            </audio>

            <script>
                const alarm = document.getElementById(
                    "spamAlarm"
                );

                alarm.play().catch(function(error) {
                    console.log(
                        "Autoplay blocked by browser.",
                        error
                    );
                });
            </script>
            """, height=65)

            st.caption(
                "If automatic sound is blocked, "
                "press Play in the audio player."
            )

            if st.button("🔊 PLAY ALARM AGAIN"):
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
            <div class="alert-box normal-box">
                <h2>✅ NORMAL MESSAGE</h2>
                <h3>NO SPAM DETECTED</h3>
                <div class="alert-light green-light"></div>
                <h3>🟢 GREEN INDICATOR</h3>
            </div>
            """, unsafe_allow_html=True)

            st.success(
                "✅ This message is classified as NORMAL."
            )

            st.caption(
                "Normal classification does not guarantee safety."
            )

        # ---------------- ML ANALYSIS ----------------
        st.divider()

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
                "Suspicious pattern detected using "
                "rule-based analysis."
            )

        st.caption(
            "ML probability is an estimate, "
            "not a guarantee of message safety."
        )


# ---------------- DETECTION HISTORY ----------------
elif page == "Detection History":

    st.title("📋 DETECTION HISTORY")

    if st.session_state.history:

        for i, item in enumerate(
            st.session_state.history,
            start=1
        ):

            st.markdown(f"**Scan {i}**")

            st.text(item["message"])

            if item["result"] == "spam":
                st.error("🔴 SPAM MESSAGE")
            else:
                st.success("🟢 NORMAL MESSAGE")

            st.caption(
                f"ML Spam Probability: "
                f"{item['probability']:.2f}%"
            )

            st.divider()

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

    This project uses Machine Learning and
    rule-based analysis to classify SMS messages.

    ### Technologies Used

    - Python
    - Streamlit
    - Scikit-learn
    - TF-IDF Vectorizer
    - Multinomial Naive Bayes

    ### Features

    - SMS Spam Detection
    - Trained Machine Learning Model
    - Bank KYC Fraud Pattern Detection
    - Lottery Scam Detection
    - Red Blinking Spam Alert
    - Green Blinking Normal Indicator
    - Alarm Sound
    - Spam Probability
    - Detection History

    ### Project Objective

    To identify potentially suspicious SMS
    messages using Machine Learning.
    """)


# ---------------- FOOTER ----------------
st.divider()

st.caption(
    "🛡️ SMS Spam Detection | AI Cyber Security Project"
)
