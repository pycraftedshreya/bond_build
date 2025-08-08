from flask import Flask, render_template, request, redirect, url_for
import os
from utils.image_gen import compose_card

app = Flask(__name__)

TEMPLATES = {
    "rakhi1": r"C:\Users\shrey\ml journey\bond_build\static\templates\rakhdi1.jpg",
    "sweets1": r"C:\Users\shrey\ml journey\bond_build\static\templates\sweets1.jpg",
    "tilak1": r"C:\Users\shrey\ml journey\bond_build\static\templates\titalk1.jpg"
}

@app.route('/')
def index():
    return render_template('index.html', templates=TEMPLATES)

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form.get('name', 'Dear Sibling')
    message = request.form.get('message', 'Happy Raksha Bandhan!')
    template_key = request.form.get('template', 'rakhi1')

    template_path = TEMPLATES.get(template_key)
    out_path, filename = compose_card(template_path, name, message)  # Removed photo_path
    card_id = filename.split('.')[0]
    return redirect(url_for('card_view', card_id=card_id))

@app.route('/card/<card_id>')
def card_view(card_id):
    card_url = url_for('static', filename=f"cards/{card_id}.png", _external=True)
    return render_template('card_view.html', card_id=card_id, card_url=card_url)

if __name__ == '__main__':
    app.run(debug=True)
