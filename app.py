from flask import Flask, request, render_template, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    try:
        completion = client.chat.completions.create(
            model="lmstudio-ai/gemma-2b-it-GGUF",
            messages=[
                {"role": "system", "content": "Assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        # Accessing the content from the message correctly
        if completion.choices and len(completion.choices) > 0:
            response = completion.choices[0].message.content
        else:
            response = "No response from the model."
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    
    return jsonify(response=response)

if __name__ == '__main__':
    app.run(debug=True)
