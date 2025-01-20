import numpy as np
import random
from flask import Flask, jsonify, request
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
app = Flask(__name__)





def create_model():
    model = Sequential()
    model.add(Dense(12, input_dim=5, activation='relu'))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer=Adam(lr=0.001), metrics=['accuracy'])
    return model
def train_model():
    X = np.array([
        [8, 1, 1, 1, 1],  # 
        [6, 1, 0, 0, 0],  # 
        [10, 1, 1, 1, 0], # 
        [7, 0, 0, 0, 0],  # l
        [12, 1, 1, 1, 1], # 
        [5, 0, 0, 0, 0],  
        [7, 1, 0, 0, 0]   
    ])
    y = np.array([1, 0, 1, 0, 1, 0, 0])
    model = create_model()
    model.fit(X, y, epochs=100, verbose=0)
    return model
model = train_model()
with open('dict.txt', 'r') as f:
    password_data = f.readlines()
vectorizer = CountVectorizer()
X_passwords = vectorizer.fit_transform(password_data)
y_passwords = np.ones(len(password_data))
password_model = MultinomialNB()
password_model.fit(X_passwords, y_passwords)
@app.route('/')
def index():
    return open('index.html').read()









@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.json.get('password', '')
    score = 0
    #logictoscore
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in '!@#$%^&*()-_=+[{]}|;:\\\'",<.>/?~' for c in password):
        score += 1
    # stren
    if score <= 2:
        strength = "Not Strong Enough"
        color = "red"
    elif score == 3:
        strength = "Almost Strong"
        color = "orange"
    elif score == 4:
        strength = "Strong"
        color = "green"
    else:
        strength = "Strongest!!!!!"
        color = "blue"
    return jsonify({"strength": strength, "color": color})
@app.route('/ai_suggestions', methods=['POST'])
def ai_suggestions():
    password = request.json.get('password', '')
    suggestions = []
    if len(password) < 8:
        suggestions.append("Consider making your password longer.")
    if not any(c.islower() for c in password):
        suggestions.append("Consider adding lowercase letters.")
    if not any(c.isupper() for c in password):
        suggestions.append("Consider adding uppercase letters.")
    if not any(c.isdigit() for c in password):
        suggestions.append("Consider adding numbers.")
    if not any(c in '!@#$%^&*()-_=+[{]}|;:\\\'",<.>/?~' for c in password):
        suggestions.append("Consider adding special characters.")
    if not suggestions:
        suggestions.append("Your password is strong enough.")
    return jsonify({"suggestions": " ".join(suggestions)})
@app.route('/generate_ai_password', methods=['GET'])
def generate_ai_password():
    random_password_index = random.randint(0, len(password_data) - 1)
    ai_generated_password = password_data[random_password_index].strip()    
    return jsonify({"password": ai_generated_password})
if __name__ == "__main__":
    app.run(debug=True)