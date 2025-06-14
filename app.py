from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

with open("data.json") as f:
    knowledge = json.load(f)

API_URL = "https://api.ai-proxy.codequotient.com/v1/chat/completions"
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDM5OTJAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.dlQMi4pzdZ8yuaaHaUO5taTTpxlY-rXPf4cwgeHypp0"

def search_context(question):
    question = question.lower()
    matches = []
    for item in knowledge:
        if any(word in item["text"].lower() for word in question.split()):
            matches.append(item["text"])
        if len(matches) >= 3:
            break
    return "\n---\n".join(matches)

@app.route("/api/", methods=["POST"])
def get_answer():
    data = request.get_json()
    question = data.get("question", "")
    context = search_context(question)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful virtual TA for a Data Science course."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{question}"}
        ]
    }

    res = requests.post(API_URL, headers=headers, json=body)
    if res.status_code == 200:
        answer = res.json()["choices"][0]["message"]["content"]
    else:
        answer = "Sorry, could not generate answer."

    return jsonify({
        "answer": answer,
        "links": [
            {"url": "https://discourse.onlinedegree.iitm.ac.in/c/courses/tds-kb/34", "text": "Check related posts"}
        ]
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)

