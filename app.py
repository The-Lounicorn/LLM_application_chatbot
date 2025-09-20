from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

app = Flask(__name__)
CORS(app)

model_name = "facebook/blenderbot-400M-distill"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

conversation_history = []
MAX_TURNS = 6

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def handle_prompt():
    try:
        data = request.get_json(force=True)
        input_text = data.get('prompt', '').strip()

        if not input_text:
            return jsonify({'error': 'Empty input'}), 400

        if len(conversation_history) > MAX_TURNS:
            conversation_history[:] = conversation_history[-MAX_TURNS:]

        formatted_history = ""
        for i, turn in enumerate(conversation_history):
            role = "User" if i % 2 == 0 else "Bot"
            formatted_history += f"{role}: {turn}</s> "

        formatted_input = f"{formatted_history}User: {input_text}</s>"
        inputs = tokenizer([formatted_input], return_tensors="pt", truncation=True)

        outputs = model.generate(
            **inputs,
            max_length=60,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7
        )

        response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
        conversation_history.append(input_text)
        conversation_history.append(response)

        return jsonify({'response': response})
    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
