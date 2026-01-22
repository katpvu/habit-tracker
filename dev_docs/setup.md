### Activating Virtual Environment

Every time you install a new package in that environment, activate the environment again

```bash
source .venv/bin/activate
```

### Check if VE is Active
```bash
which python 
```

### Update `pip` to the latest version

Normally just do this once after you create the virtual environment.
```bash
python -m pip install --upgrade pip
```

### Installing packages
```bash
pip install -r requirements.txt
```

### Saving current packages to requirements.txt file
```bash
pip freeze > requirements.txt
```

### When done working on project: Deactivate the Virtual Environment
```bash
deactivate
```

### Running the server
```bash
fastapi dev app/main.py
```

### Starting up postgresql
```bash
sudo service postgresql start
```

### Connecting to the database
```bash
psql -U habit_user -d habit_tracker
```

Password: dev_password_123