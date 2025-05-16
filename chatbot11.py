import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to get AI response for the topic recommendation
def get_ai_response(query):
    client = openai.OpenAI(api_key="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")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

# Function to get AI response for the chatbot
def get_chatbot_response(query):
    client = openai.OpenAI(api_key="YOUR_OPENAI_API_KEY_HERE") # Replace with your key
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

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    chatbot_response = get_chatbot_response(user_message)
    
    return jsonify({"response": chatbot_response})

# HTML content for the topic recommendation page
html_content = """<!DOCTYPE html>
<html>
<head>
<title>Topic Recommendation</title>
<style>
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
    display: flex;
    height: 100vh;
    background-color: #f0f4f7;
}

.container {
    display: flex;
    width: 100%;
}

.sidebar {
    background-color: #4caf50;
    padding: 20px;
    width: 20%;
    box-shadow: 2px 0 15px rgba(0, 0, 0, 0.1);
    color: white;
    transition: background-color 0.3s ease;
}

.sidebar:hover {
    background-color: #45a049;
}

.sidebar i {
    padding: 6px;
}

.sidebar h2 {
    font-size: 24px;
}

.sidebar ul {
    list-style-type: none;
    padding: 0;
}

.sidebar ul li {
    margin: 15px 0;
}

.sidebar ul li a {
    text-decoration: none;
    color: white;
    transition: color 0.3s ease;
    padding-bottom: 5px;
    display: inline-flex;
    align-items: center;
}

.sidebar ul li a:hover {
    color: #ffd700;
}

.logout-button {
    display: inline-block;
    background-color: red;
    color: white;
    padding: 10px 15px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    text-align: center;
    text-decoration: none;
    transition: background-color 0.3s ease;
    margin-top: 20px;
}

.logout-button:hover {
    background-color: darkred;
}

.content {
    flex-grow: 1;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.content h2 {
    margin-bottom: 20px;
    text-align: center;
}

.input-area {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    width: 80%;
    margin: 0 auto;
}

.input-area > div {
    width: 45%;
    margin-bottom: 10px;
}

.input-area label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.input-area input,
.input-area textarea {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    box-sizing: border-box;
    margin-bottom: 10px;
    border-radius: 5px;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.input-area input:focus,
.input-area textarea:focus {
    border-color: #4caf50;
    box-shadow: 0 0 5px #4caf50;
    outline: none;
}

.button-container {
    text-align: center;
    margin-top: 20px;
}

.recommendations {
    border: 1px solid #ccc;
    padding: 10px;
    margin-top: 20px;
    width: 60%;
    margin: 0 auto;
}

.recommendations ul {
    list-style: disc;
    padding-left: 20px;
}

.recommendations li {
    margin-bottom: 5px;
}
</style>
</head>
<body>
<div class="container">
  <aside class="sidebar">
    <section>
        <h2>Dashboard</h2>
        <ul>
            <li><a href="index.html"><i class="fas fa-home"></i>Home</a></li>
            <li><a href="#"><i class="fas fa-tasks"></i>Task Manager</a></li>
            <li><a href="#"><i class="fas fa-lightbulb"></i>Topic Recommendation</a></li>
            <li><a href="#"><i class="fas fa-check-double"></i>Topic Duplicacy Checker</a></li>
        </ul>
    </section>
  </aside>
  <div class="content">
    <h2>Topic Recommendation</h2>
    <div class="input-area">
      <div>
        <label for="areaOfInterest">Area of Interest:</label>
        <input type="text" id="areaOfInterest">
      </div>
      <div>
        <label for="specialization">Specialization:</label>
        <input type="text" id="specialization">
      </div>
      <div>
        <label for="keywords">Keywords:</label>
        <textarea id="keywords" rows="3"></textarea>
      </div>
      <div class="button-container">
        <button onclick="getRecommendations()">Recommend Topics</button>
      </div>
    </div>
    <div class="recommendations" id="recommendations">
      <!-- Recommendations will appear here -->
    </div>
  </div>
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
html_content_chatbot = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Chatbot</title>
    <style>
        /* General styles */
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        
        /* Chatbot container */
        .chatbot-container {
            width: 80%;
            height: 90vh;
            background: #1c1c1c;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            display: flex;
            flex-direction: column;
            position: relative;
            color: white;
        }
        
        /* Chat header */
        .chat-header {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px;
            border-bottom: 2px solid #444;
        }
        
        .chat-header h1 {
            margin: 0;
            font-size: 24px;
        }
        
        .chat-header .status {
            background: #4caf50;
            color: white;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 14px;
        }
        
        /* Message container */
        .messages {
            flex-grow: 1;
            overflow-y: auto;
            padding: 10px;
            margin-bottom: 15px;
        }
        
        .messages .user-message {
            text-align: right;
            margin: 5px;
        }
        
        .messages .ai-message {
            text-align: left;
            margin: 5px;
        }
        
        .message {
            max-width: 80%;
            margin: 5px;
            padding: 10px;
            border-radius: 10px;
            background-color: #444;
            display: inline-block;
        }
        
        .message.ai {
            background-color: #333;
        }
        
        /* Input area */
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        .input-area input {
            width: 80%;
            padding: 10px;
            border-radius: 5px;
            border: none;
        }
        
        .input-area button {
            background-color: #4caf50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .input-area button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>

<div class="chatbot-container">
    <div class="chat-header">
        <h1>AI Chatbot</h1>
        <span class="status">Online</span>
    </div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <input type="text" id="userMessage" placeholder="Ask a question..." />
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
async function sendMessage() {
    const userMessage = document.getElementById('userMessage').value;
    const messagesDiv = document.getElementById('messages');

    if (userMessage.trim() === "") return;

    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');
    userMessageElement.innerHTML = `<div class="message">${userMessage}</div>`;
    messagesDiv.appendChild(userMessageElement);

    document.getElementById('userMessage').value = "";

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();

    const aiMessageElement = document.createElement('div');
    aiMessageElement.classList.add('ai-message');
    aiMessageElement.innerHTML = `<div class="message ai">${data.response}</div>`;
    messagesDiv.appendChild(aiMessageElement);

    messagesDiv.scrollTop = messagesDiv.scrollHeight;  // Scroll to the latest message
}
</script>

</body>
</html>
"""

# Function to create the HTML files before starting the Flask app
def create_html_files():
    with open('abctopic_recommendation.html', 'w') as f:
        f.write(html_content)

    with open('chatbot.html', 'w') as f:
        f.write(html_content_chatbot)
# Define routes to serve the HTML files using render_template
@app.route('/topic_recommendation')
def topic_recommendation():
    return render_template('abctopic_recommendation.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')



if __name__ == '__main__':
    create_html_files()  # Create the HTML files
    app.run(debug=True, port=5001)
