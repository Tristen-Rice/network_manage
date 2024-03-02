# Network Asset Management

## Python Installation

```bash
wget https://www.python.org/ftp/python/3.9.10/Python-3.9.10.tgz
tar -xf Python-3.9.10.tgz
cd Python-3.9.10
./configure --prefix=/usr/local/python39
make && make install
ln -s /usr/local/python39/bin/python3 /usr/bin/python3
ln -s /usr/local/python39/bin/pip3 /usr/bin/pip3
```

## Python Virtual Environment Installation

- Install `virtualenv` and `virtualenvwrapper`:

  ```bash
  pip3 install virtualenv virtualenvwrapper
  ln -s /usr/local/python39/bin/virtualenvwrapper.sh /usr/bin/virtualenvwrapper.sh
  ln -s /usr/local/python39/bin/virtualenv /usr/bin/virtualenv
  ```

- Add the following lines to `~/.bashrc`:

  ```bash
  export WORKON_HOME=$HOME/.virtualenvs
  export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
  source /usr/bin/virtualenvwrapper.sh
  ```

- Create a virtual environment with a specified version:

  ```bash
  mkvirtualenv -p /usr/bin/python3 network_manage
  ```

- **Exit virtual environment**:

  ```bash
  deactivate
  ```

- **Delete virtual environment**:

  ```bash
  rmvirtualenv network_manage
  ```

## Postgres Database Initialization

- Create a new database directory:

  ```bash
  mkdir /usr/local/network_manage/
  ```

- Change the directory's owner group:

  ```bash
  chown postgres:postgres /usr/local/network_manage/
  ```

- Initialize the database directory:

  ```bash
  su - postgres -c "initdb -D /usr/local/network_manage/"
  ```

Based on network detection and switch detection to manage IP assets.

## Environment Deployment

- Python 3.9+
- Django 3.2
- React 17.0

### Backend Environment Deployment

1. Install the basic dependency packages, enter `network_manage_api` and execute:

   ```bash
   pip install -r requirements.txt
   ```

2. Django database configuration:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'device_query',
           'USER': 'root',
           'PASSWORD': '*****',
           'HOST': '127.0.0.1',
           'OPTIONS': {
               "init_command": "SET foreign_key_checks = 0;",
           },
       }
   }
   ```

   **Note: You need to create a new database in the database first:** `create database device_query`

3. Environment configuration:

   ```python
   REDIS_CONF = {
     'host': '127.0.0.1',
     'password': '123456789',
     'port': 6379
   }
   DEVICE_QUERY_QUEUE = "device:query:queue"
   DEVICE_QUERY_CRONTAB_HASH = "device:crontab:task:time"
   SERVICE_INSTALL_PATH = "/opt/network_manage/"
   SCRIPT_PATH = {
     'DEVICE_QUERY_CRON_PATH': "/opt/network_manage/bin/device_query_cron.py"
   }
   LOG_SETUP = {
     'LOG_FORMAT': "%(asctime)s %(name)s %(levelname)s %(filename)s %(message)s",
     'DATE_FORMAT': "%Y-%m-%d  %H:%M:%S",
     'SERVICE_MONITOR_PATH': "/opt/network_manage/log/serviceMonitor.log"
   }
   ```

4. Start the Django service:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver 0.0.0.0:8000
   ```

5. Enable service monitoring in the cron job:

   ```bash
   */1 * * * * /opt/network_manage/bin/service_monitor.sh >>/dev/null 2>&1
   ```

### Frontend Environment Deployment

1. Install the npm environment, search online for installation instructions.
2. Install all dependencies listed in `package.json` with one command:

   ```bash
   npm install
   ```

3. Start the npm service:

   ```bash
   npm run start
   ```

## Implemented Features

- **Device Detection**: Supports switches including Huawei, H3C, Ruijie, Cisco, Maipu (to be implemented), ZTE (to be implemented), and supports custom configuration of detection tasks.
- **Remote Terminal Login**: Supports both ssh and telnet methods.
- **Network Detection**: To be implemented.
- **Network Management**: To be implemented.
- **MAC Management**: To be implemented.

## Main Features Demonstration