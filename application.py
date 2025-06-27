from flask import Flask, render_template, request, redirect, session, send_from_directory, flash, url_for, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import uuid
import sqlite3
import requests
from werkzeug.utils import secure_filename
from PIL import Image
import re
from collections import Counter
from pdf2image import convert_from_path
import pytesseract
from dotenv import load_dotenv 
load_dotenv()
os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
app = Flask(__name__)
app.secret_key = 'secret_key_tres_forte'
app.permanent_session_lifetime = timedelta(days=30)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn    
from flask_apscheduler import APScheduler

scheduler = APScheduler()

@scheduler.task('interval', id='send_reminders_job', minutes=1)
def scheduled_send_reminders():
    with app.app_context():
        send_due_reminders()

from apscheduler.schedulers.background import BackgroundScheduler
scheduler = BackgroundScheduler()
def scheduled_send_reminders():
    print("Envoi automatique des rappels...")
    send_due_reminders()

scheduler.add_job(scheduled_send_reminders, 'interval', minutes=5)
scheduler.start()
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = "akramououissal@gmail.com"  # تأكدي يكون مفعل فـ Brevo
SENDER_NAME = "arkivo"

def send_email(subject, html_content, to_email, to_name="Utilisateur"):
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"name": SENDER_NAME, "email": SENDER_EMAIL},
        "to": [{"email": to_email, "name": to_name}],
        "subject": subject,
        "htmlContent": html_content
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Email sent:", response.status_code, response.text)
    except Exception as e:
        print("Erreur d'envoi:", e)
def send_verification_email(email, token):
    link = url_for('verify_email', token=token, _external=True)
    html = f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333;">
  <h2 style="color: #4CAF50;">Bienvenue chez Arkivo !</h2>
  <p>Merci de vous être inscrit(e) sur notre plateforme.</p>
  <p>Pour finaliser votre inscription et sécuriser votre compte, veuillez confirmer votre adresse email en cliquant sur le bouton ci-dessous :</p>
  <p style="text-align: center; margin: 30px 0;">
    <a href="{link}" style="background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
      Vérifier mon adresse email
    </a>
  </p>
  <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
  <p><a href="{link}" style="color: #4CAF50;">{link}</a></p>
  <p>Nous sommes ravis de vous compter parmi nous !</p>
</div>
"""
    send_email("Vérification de votre compte", html, email)
def send_password_reset_email(email, token):
    link = url_for('reset_password', token=token, _external=True)
    html = f"""
<div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; color: #333;">
  <h2 style="color: #2c3e50;">Réinitialisation de votre mot de passe</h2>
  <p>Vous avez demandé à réinitialiser votre mot de passe. Pas de panique !</p>
  <p>Pour créer un nouveau mot de passe, cliquez simplement sur le bouton ci-dessous :</p>
  <p style="text-align: center; margin: 30px 0;">
    <a href="{link}" style="background-color: #28a745; color: white; padding: 15px 25px; text-decoration: none; border-radius: 5px; font-weight: bold;">
      Réinitialiser mon mot de passe
    </a>
  </p>
  <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
  <p><a href="{link}" style="color: #FF5722;">{link}</a></p>
  <hr>
  <p style="font-size: 0.9em; color: #777;">Si vous n'avez pas demandé cette réinitialisation, ignorez simplement ce message.</p>
  <p style="font-size: 0.9em;">Merci de faire confiance à <strong>Arkivo</strong> !</p>
</div>
"""
    send_email("Réinitialisation du mot de passe", html, email)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')
@app.route('/register', methods=['POST'])
def register():
    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']
    hashed = generate_password_hash(password)

    conn = get_db()
    cur = conn.cursor()

    # Vérifier si l'email est déjà utilisé
    cur.execute("SELECT id FROM users WHERE email=?", (email,))
    if cur.fetchone():
        flash("Email déjà utilisé.", "error")
        conn.close()
        return redirect('/')

    # Créer l'utilisateur
    cur.execute("INSERT INTO users (fullname, email, password, is_verified) VALUES (?, ?, ?, ?)",
                (fullname, email, hashed, 0))
    user_id = cur.lastrowid

    # Créer le token de vérification
    token = str(uuid.uuid4())
    cur.execute("INSERT INTO email_verification (user_id, token) VALUES (?, ?)", (user_id, token))

    # 🔽 Créer les dossiers par défaut
    default_folders = ['Eau', 'Électricité', 'Assurance']
    for name in default_folders:
        cur.execute("INSERT INTO folders (name, user_id) VALUES (?, ?)", (name, user_id))

    # Commit & close
    conn.commit()
    conn.close()

    # Envoyer l'email de vérification
    send_verification_email(email, token)
    flash("Inscription réussie ! Vérifiez votre email.", "success")
    return redirect('/')
@app.route('/verify-email')
def verify_email():
    token = request.args.get('token')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM email_verification WHERE token=?", (token,))
    row = cur.fetchone()
    if row:
        cur.execute("UPDATE users SET is_verified=1 WHERE id=?", (row['user_id'],))
        cur.execute("DELETE FROM email_verification WHERE user_id=?", (row['user_id'],))
        conn.commit()
        flash("Email vérifié !", "success")
    else:
        flash("Lien invalide ou expiré.", "error")
    conn.close()
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email=?", (email,))
    user = cur.fetchone()
    conn.close()
    if user and check_password_hash(user['password'], password):
        if not user['is_verified']:
            flash("Vérifiez votre email d'abord.", "error")
            return redirect('/')
        session['user_id'] = user['id']
        session['fullname'] = user['fullname']
        session['user_email'] = user['email']
        return redirect('/dashboard')
    flash("Identifiants invalides.", "error")
    return redirect('/')
