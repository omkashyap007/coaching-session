# Coaching Session App

A Django web app where **students can book coaching sessions with experts**, manage availability, and prevent session overlap.

---

## 🚀 Features

- Register/Login as **Student** or **Expert**
- Students can:
  - View experts
  - Create coaching sessions
  - Join and complete sessions
- Prevents **overlapping session times**
- Simple UI and easy workflow

---

## ⚙️ Setup & Installation

```sh
# 1️⃣ Create virtual environment
python -m venv coaching_env

# 2️⃣ Activate virtual environment
# Windows
coaching_env\Scripts\activate
# Mac/Linux
source coaching_env/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Run migrations
python manage.py migrate

# 5️⃣ Start server
python manage.py runserver

## System Design

**Link1:**  
![Link1](https://raw.githubusercontent.com/omkashyap007/coaching-session/master/images/application_structure.png)

**Link2:**  
![Link2](https://raw.githubusercontent.com/omkashyap007/coaching-session/master/images/system_design.png)
