# scoring
Project for P2P/IoT-project course.  

Look in the wiki to see how the raspberries should be setup.



## Settings files
```
instance/settings.py

DEBUG = False
SERVER_NAME = '192.168.42.X:8000'
SESSION_COOKIE_NAME = '192.168.42.X:8000'
SESSION_COOKIE_DOMAIN = '192.168.42.X:8000'
SCORING_APP_TYPE = 'SPECTATOR'
```

```
instance/judge.py

DEBUG = True
SERVER_NAME = 'localhost:7000'
SESSION_COOKIE_NAME = 'localhost:7000'
SESSION_COOKIE_DOMAIN = 'localhost:7000'
SCORING_APP_TYPE = 'JUDGE'
```

```
instance/updates.py

DEBUG = False
SERVER_NAME = '192.168.4.X:5000'
SESSION_COOKIE_NAME = '192.168.4.X:5000'
SESSION_COOKIE_DOMAIN = '192.168.4.X:5000'
SCORING_APP_TYPE = 'UPDATES'
```
