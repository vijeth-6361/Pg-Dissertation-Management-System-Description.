import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to get AI response
def get_ai_response(query):
    client = openai.OpenAI( api_key="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")  # Use your actual API key
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

@app.route('/')
def index():
    return render_template('topic_recommendation.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    area = data.get('areaOfInterest', '')
    specialization = data.get('specialization', '')
    keywords = data.get('keywords', '')
    
    query = f"Suggest well-structured research topics related to Area of Interest: {area}, Specialization: {specialization}, and Keywords: {keywords}. Provide specific topics with objectives."
    
    ai_response = get_ai_response(query)
    
    return jsonify({"recommendations": ai_response.split("\n")})

# HTML content for the topic recommendation page
topic_recommendation_html_content = """<!DOCTYPE html>
<html>
<head>
<title>Topic Recommendation</title>
<style>
/* Add your CSS styles here */
body { font-family: Arial, sans-serif; }
</style>
</head>
<body>
<div>
  <h1>Topic Recommendation</h1>
  <form id="recommendation-form">
    <label>Area of Interest:</label>
    <input type="text" id="areaOfInterest">
    <label>Specialization:</label>
    <input type="text" id="specialization">
    <label>Keywords:</label>
    <textarea id="keywords"></textarea>
    <button type="button" onclick="getRecommendations()">Recommend Topics</button>
  </form>
  <div id="recommendations"></div>
</div>

<script>
async function getRecommendations() {
  const areaOfInterest = document.getElementById('areaOfInterest').value;
  const specialization = document.getElementById('specialization').value;
  const keywords = document.getElementById('keywords').value;
  const recommendationsDiv = document.getElementById('recommendations');

  const response = await fetch('/recommend', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ areaOfInterest, specialization, keywords }),
  });

  const data = await response.json();
  recommendationsDiv.innerHTML = `<ul>${data.recommendations.map(topic => `<li>${topic}</li>`).join('')}</ul>`;
}
</script>
</body>
</html>
"""

# HTML content for the chatbot page
chatbot_html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        /* Add your chatbot styles here */
        body { font-family: Arial, sans-serif; background: linear-gradient(45deg, #0f0c29, #302b63, #24243e); }
    </style>
</head>
<body>
    <div class="chatbot-container">
        <div class="chat-header">
            <h2>AI Chatbot</h2>
        </div>
        <div id="chat-box"></div>
        <div class="chat-input-container">
            <input type="text" id="user-input" placeholder="Type a message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        function sendMessage() {
            let userInput = document.getElementById("user-input").value;
            if (!userInput) return;

            let chatBox = document.getElementById("chat-box");

            let userMessage = document.createElement("div");
            userMessage.className = "chat-message user-message";
            userMessage.innerHTML = `<span>${userInput}</span>`;
            chatBox.appendChild(userMessage);

            fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userInput })
            })
            .then(response => response.json())
            .then(data => {
                let botMessage = document.createElement("div");
                botMessage.className = "chat-message bot-message";
                botMessage.innerHTML = `<span>${data.response}</span>`;
                chatBox.appendChild(botMessage);

                chatBox.scrollTop = chatBox.scrollHeight;
            });

            document.getElementById("user-input").value = "";
        }
    </script>
</body>
</html>
"""

# Function to create both HTML files before starting the Flask app
def create_html_files():
    with open('topic_recommendation.html', 'w') as f:
        f.write(topic_recommendation_html_content)

    with open('chatbot.html', 'w') as f:
        f.write(chatbot_html_content)

if __name__ == '__main__':
    create_html_files()  # Create both HTML files
    app.run(debug=True)
