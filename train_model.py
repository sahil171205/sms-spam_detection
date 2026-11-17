
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Step 1: Load Dataset
df = pd.read_csv(
    "SMSSpamCollection",
    sep="\t",
    names=["label", "message"]
)

# Step 2: Prepare Data
df = df.dropna()

X = df["message"]
y = df["label"]

# Step 3: Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Step 4: TF-IDF Feature Extraction
vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Step 5: Train Naive Bayes Model
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Step 6: Model Prediction
y_pred = model.predict(X_test_tfidf)

# Step 7: Evaluation
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)
print(classification_report(y_test, y_pred))

# Step 8: Save Model
with open("spam_model.pkl", "wb") as file:
    pickle.dump({
        "model": model,
        "vectorizer": vectorizer
    }, file)

print("Model trained and saved successfully!")
