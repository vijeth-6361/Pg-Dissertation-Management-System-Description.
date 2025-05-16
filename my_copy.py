import openai
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Replace with your actual OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"  

def get_ai_response(query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content


@app.route('/')
def index():
    return render_template('plagiarism_check.html') #Updated template name

@app.route('/check', methods=['POST'])
def check_plagiarism():
    data = request.json
    title = data.get('title', '')
    description = data.get('description', '')

    query = f"""Analyze the following text for potential plagiarism:

Title: {title}
Description: {description}

Respond with:
* A general assessment of plagiarism risk (e.g., "High risk," "Low risk," "Unclear").
* A brief explanation of why the assessment is made.  Focus on the potential for unoriginality, not the precise sources.  Do not attempt to find specific sources or calculate percentages.
"""
    ai_response = get_ai_response(query)
    return jsonify({"analysis": ai_response})


if __name__ == '__main__':
    app.run(debug=True)
