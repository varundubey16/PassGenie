import os
import random
import math
import matplotlib
matplotlib.use('Agg') #prevent flask crash -https://www.reddit.com/r/learnpython/comments/16tzyr3/error_message_matplotlib_is_currently_using_agg/ 
import matplotlib.pyplot as plt
#import seaborn
import seaborn as sns
import pandas as pd
from flask import Flask, jsonify, request, send_file
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

#v4 new additon is io cuz crash of matplot png generation
import io
from sklearn.linear_model import LogisticRegression




app = Flask(__name__)
#rockucmpilied loadin pandas
#
df = pd.read_csv('pasexamples.txt')
#feature engineering
CHARS = "!@#$%^&*_-+=<>?/"
df['len'] = df['password'].astype(str).apply(len)
df['low'] = df['password'].astype(str).apply(lambda p: 1 if any(c.islower() for c in p) else 0)
df['up'] = df['password'].astype(str).apply(lambda p: 1 if any(c.isupper() for c in p) else 0)
df['digi'] = df['password'].astype(str).apply(lambda p: 1 if any(c.isdigit() for c in p) else 0)
df['specl'] = df['password'].astype(str).apply(lambda p: 1 if any(c in CHARS for c in p) else 0)
#
ab = df[['len', 'low', 'up', 'digi', 'specl']]
cd = df['strength']
#ppji
#80-20 default
ab_train, ab_test, cd_train, cd_test = train_test_split(ab, cd, test_size=0.2, random_state=42)
vraunzclassify = DecisionTreeClassifier() 
#modelTEST11 = LogisticRegression()
vraunzclassify.fit(ab_train, cd_train)
# --- seaborn performnce plot
# confusion matrix show eval
cd_pred = vraunzclassify.predict(ab_test)
label = ["Weak", "Medium", "Strong", "Very Strong"]
label = [l for l in label if l in cd_test.unique()]
cm = confusion_matrix(cd_test, cd_pred, labels=label)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=label, yticklabels=label)
plt.title('Model Accuracy Evaluation')
plt.ylabel('Actual Strength')
plt.xlabel('Predicted Strength')
plt.tight_layout()
plt.savefig('modeleval.png') # saved once when app starts to prove training works
plt.close()




#commented inhtml,userkyakregadekh ke....
def getentro(pword): 
    pool = 0
    low, upp, num, spc = False, False, False, False
    for c in pword:
        if c.islower(): low = True
        if c.isupper(): upp = True
        if c.isdigit(): num = True
        if c in CHARS: spc = True
    if low: pool += 26
    if upp: pool += 26
    if num: pool += 10
    if spc: pool += len(CHARS)
    if pool == 0: 
        return 0
    return round(len(pword) * math.log2(pool), 2)
@app.route('/')
def home():
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()
@app.route('/chartie')
#plotter test for user showing def chartie():
def chartie():


    #if os.path.exists('livechart.png'):
    #    return send_file('livechart.png', mimetype='image/png')
    #return 'none', 404
    # -io work
    length = int(request.args.get('len', 0))
    lower = int(request.args.get('low', 0))
    upper = int(request.args.get('up', 0))
    digit = int(request.args.get('dig', 0))
    special = int(request.args.get('spc', 0))
    clr = request.args.get('clr', 'gray')
    plt.figure(figsize=(4.5, 2.2))
    plt.bar(["Length", "Lowercase", "Uppercase", "Digits", "Specialchar"], [length, lower, upper, digit, special], color=clr)  
    plt.ylabel("Each Qty")
    plt.tight_layout()
    img_buf = io.BytesIO()
    plt.savefig(img_buf, format='png')
    img_buf.seek(0)
    plt.close()
    return send_file(img_buf, mimetype='image/png')
@app.route('/checkpas', methods=['POST'])
def checkpas():
    req = request.get_json()
    p = req.get('password', '')
    if p == '':
        return jsonify({
            "strength": "Type a Password.....",
            "color": "gray",
            "entropy": 0,
            "plot_url": ""
        })
    length = len(p)
    lower = 1 if any(c.islower() for c in p) else 0
    upper = 1 if any(c.isupper() for c in p) else 0
    digit = 1 if any(c.isdigit() for c in p) else 0
    special = 1 if any(c in CHARS for c in p) else 0  
    # --- COMMENTED OUT ORIGINAL PREDICTION ---
    # res = vraunzclassify.predict([[length, lower, upper, digit, special]])[0]
    # --- NEW PREDICTION CODE (FIXES SKLEARN WARNING) ---
    inpudta = pd.DataFrame([[length, lower, upper, digit, special]], 
                              columns=['len', 'low', 'up', 'digi', 'specl'])
    res = vraunzclassify.predict(inpudta)[0]    
    colors = {"Weak": "red", "Medium": "orange", "Strong": "blue", "Very Strong": "green"}
    clr = colors.get(res, "gray")
    ent = getentro(p)

    # --- COMMENTED OUT ORIGINAL FILE SAVING & RETURN ---
    # #plotnow (keeping your original livechart code running on every keystroke exactly as requested)
    # plt.figure(figsize=(4.5, 2.2))
    # plt.bar(["Length", "Lowercase", "Uppercase", "Digits", "Specialchar"], [length, lower, upper, digit, special], color=clr)  
    # plt.ylabel("Matches")
    # plt.tight_layout()
    # plt.savefig('livechart.png')
    # plt.close()
    # return jsonify({
    #     "strength": res,
    #     "color": clr,
    #     "entropy": ent,
    #     "plot_url": "/chartie?rand=" + str(random.random())
    # })
    # --- NEW RETURNING CODE (FIXES WINDOWS FILE-LOCK CRASH) ---
    plot_url = f"/chartie?len={length}&low={lower}&up={upper}&dig={digit}&spc={special}&clr={clr}&rand={random.random()}"
    return jsonify({
        "strength": res,
        "color": clr,
        "entropy": ent,
        "plot_url": plot_url
    })
@app.route('/aisggsts', methods=['POST'])
def aisggsts():
    data = request.get_json()
    pwd = data.get('password', '')
    tips = []
    if len(pwd) < 8:
        tips.append("Make it longer! (at least 8 chars),")
    if not any(c.islower() for c in pwd): tips.append("Add lowercase,")
    if not any(c.isupper() for c in pwd): tips.append("Add uppercase,")
    if not any(c.isdigit() for c in pwd): tips.append("Add numbers,")
    has_spc = any(c in CHARS for c in pwd)
    if not has_spc: 
        tips.append("Add special chars")
    if not tips:
        return jsonify({"suggestions": "Password is solid boy!"})
    return jsonify({"suggestions": " ".join(tips)})
@app.route('/geaipssd', methods=['GET'])
def pasgen():
    abc = "abcdefghijklmnopqrstuvwxyz"
    caps = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    nums = "0123456789"
    syms = "!@#$%^&*_-"
    arr = [random.choice(abc), random.choice(caps), random.choice(nums), random.choice(syms)]
    all_chars = abc + caps + nums + syms
    for _ in range(10):
        arr.append(random.choice(all_chars))
    random.shuffle(arr)
    return jsonify({"password": "".join(arr)})
if __name__ == "__main__":
    app.run(debug=True)#
   #app.run(debug=False) 
