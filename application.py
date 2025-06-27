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
@app.route('/logout')
def logout():
    session.clear()
    flash("Déconnecté.", "info")
    return redirect('/')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE email=?", (email,))
        user = cur.fetchone()
        if user:
            token = str(uuid.uuid4())
            cur.execute("DELETE FROM password_reset WHERE user_id=?", (user['id'],))
            cur.execute("INSERT INTO password_reset (user_id, token) VALUES (?, ?)", (user['id'], token))
            conn.commit()
            send_password_reset_email(email, token)
        flash("Si cet email existe, un lien a été envoyé.", "info")
        conn.close()
        return redirect('/')
    return render_template('forgot.html')
@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html', token=request.args.get('token'))

    token = request.form['token']
    password = request.form['password']
    confirm_password = request.form['confirm_password']

    # Vérifie si les deux mots de passe correspondent
    if password != confirm_password:
        flash("Mots de passe non indentiques.", "error")
        return render_template('reset_password.html', token=token)

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM password_reset WHERE token=?", (token,))
    row = cur.fetchone()

    if row:
        hashed = generate_password_hash(password)
        cur.execute("UPDATE users SET password=? WHERE id=?", (hashed, row['user_id']))
        cur.execute("DELETE FROM password_reset WHERE user_id=?", (row['user_id'],))
        conn.commit()
        flash("Mot de passe réinitialisé !", "success")
        conn.close()
        return redirect('/')
    else:
        flash("Lien invalide ou expiré.", "error")
        conn.close()
        return redirect('/')
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import os
import fitz  # PyMuPDF
from werkzeug.utils import secure_filename
from io import BytesIO

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def preprocess_image(image):
    # تحويل لصورة رمادية
    image = image.convert('L')
    # رفع التباين
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # إزالة التشويش بخاصية MedianFilter
    image = image.filter(ImageFilter.MedianFilter(size=3))
    # Thresholding: جرب تغير 120 حسب جودة الصورة
    image = image.point(lambda x: 0 if x < 120 else 255, '1')
    return image
def extract_text_from_image_file(file_stream):
    try:
        image = Image.open(file_stream)
        image = preprocess_image(image)
        # psm 6: assume a uniform block of text
        text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
        return text
    except Exception as e:
        print("❌ OCR Error:", e)
        return ""
def extract_text_from_file(path):
    ext = path.lower().split('.')[-1]
    if ext in ['jpeg', 'jpg', 'png']:
        try:
            image = Image.open(path)
            image = preprocess_image(image)
            text = pytesseract.image_to_string(image, lang='fra', config='--psm 6 --oem 3')
            return text
        except Exception as e:
            print("❌ OCR Image Error:", e)
            return ""
    elif ext == 'pdf':
        text = ""
        try:
            doc = fitz.open(path)
            for page in doc:
                pix = page.get_pixmap(dpi=400)  # رفع دقة الصورة
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img = preprocess_image(img)
                page_text = pytesseract.image_to_string(img, lang='fra', config='--psm 6 --oem 3')
                text += page_text + "\n"
            return text
        except Exception as e:
            print("❌ OCR PDF Error:", e)
            return ""
    else:
        return ""
from utils_classifier import classify_document
import uuid

@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('Aucun fichier sélectionné.', 'error')
        return redirect(url_for('files'))

    file = request.files['file']
    if file.filename == '':
        flash('Nom de fichier invalide.', 'error')
        return redirect(url_for('files'))
    original_filename = secure_filename(file.filename)
    ext = os.path.splitext(original_filename)[1].lower()

    # توليد اسم فريد لتفادي تعارض الملفات
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
