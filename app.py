import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to get AI response
def get_ai_response(query):
    client = openai.OpenAI(api_key="")
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
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>
<body>
<div class="container">
  <aside class="sidebar">
    
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

  if (data.recommendations.length > 5) {
    createDropdown(data.recommendations);
  } else {
    recommendationsDiv.innerHTML = `<ul>${data.recommendations.map(topic => `<li>${topic}</li>`).join('')}</ul>`;
  }
}

function createDropdown(recommendations) {
  const recommendationsDiv = document.getElementById('recommendations');
  const select = document.createElement('select');
  recommendations.forEach(topic => {
    const option = document.createElement('option');
    option.value = topic;
    option.text = topic;
    select.appendChild(option);
  });
  recommendationsDiv.innerHTML = '';
  recommendationsDiv.appendChild(select);
}
</script>
</body>
</html>

"""

# Function to create the HTML file before starting the Flask app
def create_html_file():
    with open('topic_recommendation.html', 'w') as f:
        f.write(html_content)

if __name__ == '__main__':
    create_html_file()  # Create the HTML file
    app.run(debug=True)