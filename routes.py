from flask import Flask, render_template, request, flash
from forms import ContactForm

app = Flask(__name__)

app.secret_key = 'development key'

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    return 'Form posted.'

  elif request.method == 'GET':
    return render_template('contact.html', form=form)
