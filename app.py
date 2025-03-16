from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__)

def load_qa_data():
    with open('questions_answers.json', 'r', encoding='utf-8') as file:
        return json.load(file)

qa_data = load_qa_data()

# Function to clean and format text
def clean_text(answer):
    # Remove <PAD> tags and extra whitespaces
    answer = re.sub(r'<pad>', '', answer)
    answer = re.sub(r'pad>', '', answer)
    answer = re.sub(r'\s+', ' ', answer)
    answer = answer.strip()
    return answer

# Function to find a response to the user's query
def get_bot_response(user_input):
    cleaned_input = clean_text(user_input.lower())

    for entry in qa_data:
        cleaned_question = clean_text(entry['question'].lower())
        if cleaned_input in cleaned_question:
            return {
                'response': entry['answer'],
            }

    return {
        'response': "Sorry, I couldn't find an answer. Please ask something else.",
        'sources': []
    }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    # Get the user's message from the POST request
    user_message = request.json.get('message')

    # Get the response based on the user's input
    bot_response = get_bot_response(user_message)
    
    # Return the response as a JSON object
    return jsonify(bot_response)

if __name__ == '__main__':
    app.run(debug=True)