from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///phone_book.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

@app.route('/add', methods=['POST'])
def add_contact():
    name = request.form['name']
    phone = request.form['phone']
    
    # Проверяем, существует ли уже контакт с таким именем или номером телефона
    existing_contact = Contact.query.filter((Contact.name == name) | (Contact.phone == phone)).first()
    if existing_contact:
        return "Такой контакт уже существует"

    new_contact = Contact(name=name, phone=phone)
    db.session.add(new_contact)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    phone_book = Contact.query.all()
    return render_template('index.html', phone_book=phone_book)
@app.route('/clear', methods=['POST'])
def clear_contacts():
    Contact.query.delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)