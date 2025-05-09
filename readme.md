# Alasatizah 

Alasatizah is a Django-based web application built for connecting **Organizations** with verified **Hafeez** across Bangladesh. It’s a secure, scalable platform that allows Hafeez to register, manage their profiles, and receive job opportunities from Organizations. Styled using **Tailwind CSS** for a clean and modern UI.

## Features

- 🔐 Secure registration and authentication for Hafeez and Organizations
- 📄 Profile management and verification system for Hafeez
- 🏢 Organization dashboard to post, manage, and hire Hafeez
- 🔎 Advanced search and filtering options
- 📩 Messaging or contact system between both parties
- 🎨 Fully responsive UI using Tailwind CSS
- 🌐 Admin dashboard for platform monitoring

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Frontend:** HTML + Tailwind CSS
- **Database:** PostgreSQL (or SQLite for local dev)
- **Authentication:** Session-based
- **Deployment:** Docker-ready / Compatible with DigitalOcean or any VPS

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js & npm (for Tailwind CSS build)
- PostgreSQL (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/alasatizah.git
   cd alasatizah
   ```
2. **Create a virtual environment and activate it**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4. **Install frontend dependencies and build Tailwind CSS**
    ```bash
    npm install
    npm run build
    ```
5. **Apply migrations**
    ```bash
    python manage.py migrate
    ```
6. **Create a superuser**
    ```bash
    python manage.py createsuperuser
    ```
7. **Run the development server**
    ```bash
    python manage.py runserver
    ```



