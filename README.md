# 👗 AI-Powered Fashion Web Application

This web application delivers a cutting-edge fashion experience that combines the functionality of a full-featured e-commerce platform with the power of AI. It allows users to explore, customize, and purchase fashion items effortlessly.

## ✨ Key Features

- 🛍 **E-Commerce Platform**  
  Browse and shop a wide variety of products — similar to popular platforms like Myntra.

- 🎨 **Custom Outfit Builder**  
  Design and save personalized outfits using an interactive fashion designer tool.

- 🤖 **AI-Powered Outfit Suggestion**  
  Get intelligent outfit recommendations based on gender, occasion, weather, style, and color using Google Gemini API.

- 🔐 **User Authentication & Authorization**  
  Secure login system with Django’s built-in authentication.

- 🛒 **Shopping Cart**  
  Seamless cart and checkout experience.

---

## ⚙️ Setup Instructions

### 📌 Prerequisites

- Python 3.x
- pip (Python package manager)
- A valid **Google API Key** for the Gemini model

---

### 🚀 Installation

#### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_folder>
```

#### 2. Create & Activate Virtual Environment (Recommended)

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 3. Install Project Dependencies

```bash
pip install -r requirements.txt
```

> **Required packages** (in `requirements.txt`):
```
Django
python-dotenv
google-generativeai
Pillow
```

---

### 🔐 Configure Environment Variables

Create a `.env` file in the project root (same level as `manage.py`) and add:

```env
GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
```

---

### 📧 Configure Email Settings

Update `fashion/settings.py` with your SMTP credentials:

```python
# fashion/settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # or your preferred SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@example.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
DEFAULT_FROM_EMAIL = 'your_email@example.com'
```

---

### 🛠 Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 👤 Create Superuser (Admin Panel Access)

```bash
python manage.py createsuperuser
```

---

### 🧪 Run the Development Server

```bash
python manage.py runserver
```

Visit the app in your browser at:  
👉 **http://127.0.0.1:8000/**

---

## 🧩 Optional Tips

- Use `python manage.py runserver 0.0.0.0:8000` to make the app accessible on your local network.
- Access the admin panel at `http://127.0.0.1:8000/admin/`.
- Store sensitive credentials securely (use `.env` and never commit it).

---

## 📁 Project Structure (Simplified)

```
├── authentication/           # Handles user login, registration, authentication logic
│   └── ...                   # (views.py, models.py, urls.py, etc.)
├── fashion/                  # Django project settings and main URLs
│   └── ...                   # (settings.py, urls.py, wsgi.py, asgi.py)
├── media/
│   └── product_images/       # Uploaded product image files
├── static/                   # Static assets (CSS, JS, images)
│   └── ...                   
├── templates/                # HTML templates for rendering UI
│   └── ...                   
├── README.md                # Project overview and setup guide
├── requirements.txt
├── api.txt                   # Likely contains the Gemini API key or related config (move content to .env)
├── c.csv                     # CSV data (could be product data or user preferences)
├── db.sqlite3                # SQLite database file (used in development)
├── ini.env                   # Environment variables (should be renamed to `.env`)
├── manage.py                 # Django’s CLI utility for administrative tasks

```


