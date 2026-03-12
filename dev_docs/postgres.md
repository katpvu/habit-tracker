## Create a new database

```bash
# connec to PostgreSQL as the postgres superuser
sudo -u postgres psql
```

```postgres
CREATE DATABASE habit_tracker;

CREATE USER habit_user WITH password 'dev_password_123';

GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_user;

\c habit_tracker

GRANT ALL ON SCHEMA public TO habit_user;

\l
\du
\q
```

Connect to database as habit_user
```bash
psql -h localhost -U habit_user -d habit_tracker
```

Note: Include `-h localhost` if you haven't updated PostgreSQL Authentication (pg_hba.conf)  
```
  # "local" is for Unix domain socket connections only. Change peer -> md5
  local   all             all                                     md5
```

Restart postgres after updating this configuration: `sudo service postgres restart`


Enter password 'dev_password_123'

