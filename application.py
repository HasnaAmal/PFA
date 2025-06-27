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
