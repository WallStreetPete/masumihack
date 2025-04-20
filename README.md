# Aeruko - Masumi Hackathon Submission


---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Variables](#environment-variables)
  - [Front-End Setup](#front-end-setup)
  - [Back-End & Agents Setup](#back-end--agents-setup)
- [Scripts](#scripts)
- [License](#license)

---

## Features

- Modern Next.js front-end
- Python server for agent orchestration
- Email crew agent (Apollo)
- Easy local development setup

---

## Tech Stack

- **Front-End:** [Next.js](https://nextjs.org/)
- **Back-End:** Python 3.x
- **Agent Scripts:** Python

---

## Project Structure

```
/
├── frontend/                # Next.js app
│   ├── .env.example
│   └── ...
├── backend/                 # Python server and agents
│   ├── .env.example
│   ├── masumi_deploy.py
│   └── apollo_email_crew.py
└── README.md
```

---

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) (v18+ recommended)
- [npm](https://www.npmjs.com/) (comes with Node.js)
- [Python 3.12](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/) (recommended)

---

### Environment Variables

Both the front-end and back-end require environment variables.

1. **Copy the example env files:**

   ```bash
   # For frontend
   cp frontend/.env.example frontend/.env

   # For backend
   cp backend/.env.example backend/.env
   ```

2. **Edit the `.env` files** and fill in the required values.

---

### Front-End Setup

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**

   ```bash
   npm run dev
   ```

   The app will be running at [http://localhost:3000](http://localhost:3000).

---

### Back-End & Agents Setup

1. **Navigate to the backend directory:**

   ```bash
   cd backend
   ```

2. **Create and activate a Python virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Deploy agents:**

   ```bash
   python masumi_deploy.py
   ```

5. **Start the Python server (Apollo Email Crew):**

   ```bash
   python apollo_email_crew.py
   ```

---

## Scripts

- **Front-End**
  - `npm run dev` — Start Next.js dev server

- **Back-End**
  - `python masumi_deploy.py` — Deploy agents
  - `python apollo_email_crew.py` — Start the Apollo email agent/server

---

## License

This project is for educational and hackathon purposes.

---

**Happy Hacking! 🚀**

---

Let me know if you want to add more sections or details!
