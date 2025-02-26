# Django + React Project Setup

## 📂 Project Structure

```
project-root/
├── backend/          # Django project
│    ├── manage.py   # Django entry point
├── frontend/        # React app
│    ├── package.json # React dependencies
│    ├── node_modules/ 
│    └── src/        # React source code
├── package.json     # Root-level scripts/tools
└── .venv/           # Python virtual environment
```

## 🛠️ Setup Instructions

### 1. Clone the Project

```bash
git clone your-repo-url
cd project-root
```

### 2. Set Up Django Backend

1. Ensure **Python** is installed.
2. Create a virtual environment and activate it:

   **Linux/macOS:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

4. Run database migrations:

```bash
python backend/manage.py migrate
```

5. Start the Django server:

```bash
python backend/manage.py runserver
```

### 3. Set Up React Frontend

1. Ensure **Node.js** and **npm** are installed.
2. Navigate to the `frontend` folder and install dependencies:

```bash
cd frontend
npm install
```

3. Start the React development server:

```bash
npm start
```

## ✅ Common Commands

| Action                         | Command                           |
|--------------------------------|-----------------------------------|
| Start Django server            | `python backend/manage.py runserver` |
| Start React app                | `cd frontend && npm start`         |
| Install React packages         | `cd frontend && npm install <pkg>` |
| Install root-level packages    | `npm install <pkg> --save-dev`     |
| Run both servers concurrently  | `npm run dev`                      |

## Cleanup

- **Stop servers:** `CTRL + C`
- **Deactivate virtualenv:** `deactivate` (Linux/macOS) or `.venv\Scripts\deactivate` (Windows)

## Notes

- Ensure Python, Node.js, and npm are installed on your system.
