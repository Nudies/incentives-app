#Virtual Incentives

##Local Setup
```
git clone https://github.com/Nudies/incentives-app.git```  
cd incentives-app/  
touch app.db test.db config.py  
sudo pip install -r requirements.txt  
```  

You will want to edit your config.py to look something like this.  
```
import os  
  
_basedir = os.path.abspath(os.path.dirname(__file__))  
  
#This keeps emails form going out  
TESTING = True  
DEBUG = False  
  
ADMINS = frozenset(['youremail@yourdomain.com'])  
SECRET_KEY = 'key.txt'  
  
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'app.db')  
SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')  
  
DATABASE_CONNECT_OPTIONS = {}  
  
CSRF_ENABLED = True  
CSRF_SESSION_KEY = "change-to-something-impossible-to-guess"  
```  
  
To create our database tables run `python shell.py` then at the prompt put `>>> db.create_all()`.  
  
Next lets run our local server  
```python run.py```  
  
Direct your browser to `localhost:5000` and you should be running.  
  
##Production  
For production I am using Ubuntu 14.04 x64 virtual server running Apache with mod_wsgi.  
You can find a good tutorial [here](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps) provided by digitalocean. I found I had to MacGyver it a little bit to get it running, but it is pretty straight forward.

For a mail I am using postfix as a send-only SMTP server. Routing any incoming mail to another address.
  
Don't bother running `setup.sh` as it has some issues and I am to lazy to fix them atm.  
