from flask import Flask, render_template, request, jsonify
from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration, BlipForQuestionAnswering

# Initialize the Flask app
app = Flask(__name__, static_folder="static", template_folder="template")

# Load the BLIP model and processor for both captioning and question answering
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
qa_model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for processing the uploaded image and generating caption
@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    # Open the image file
    image = Image.open(file.stream)
    
    # Preprocess the image for captioning
    inputs = processor(images=image, return_tensors="pt")
    out = caption_model.generate(**inputs)
    
    # Decode the generated caption
    caption = processor.decode(out[0], skip_special_tokens=True)
    
    return jsonify({"caption": caption})

# Route for processing questions about the uploaded image
@app.route('/answer', methods=['POST'])
def answer():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    question = request.form.get('question', '').strip()
    
    if not question:
        return jsonify({"error": "No question provided"})
    
    # Open the image file
    image = Image.open(file.stream)
    
    # Preprocess the image for question answering
    inputs = processor(images=image, text=question, return_tensors="pt")
    answer = qa_model.generate(**inputs)
    
    # Decode the answer
    answer_text = processor.decode(answer[0], skip_special_tokens=True)
    
    return jsonify({"answer": answer_text})

if __name__ == "__main__":
    app.run(debug=True)