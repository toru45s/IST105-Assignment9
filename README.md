# Cisco DNA Center Django Dashboard

This Django web application integrates with Cisco DNA Center's REST API to:

- Authenticate and retrieve an access token
- List network devices
- Display interface details for a selected device
- Log each action (with timestamp, IP, and result) into MongoDB

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/dnac-dashboard.git
cd dnac-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a .env file in your root project directory (same level as manage.py):

```
MONGO_URI=mongodb://localhost:27017/
```

### 5. Start the server

```bash
python manage.py runserver
```
