References:

# Install app deps
```
pip3 install -r requirements.txt
```

# Setting static IP address
https://pimylifeup.com/raspberry-pi-static-ip-address/


# Installing Supervisor
http://supervisord.org/installing.html

Supervisord config is copied to /etc/supervisord/conf.d/
```
sudo cp garage_supervisor.conf /etc/supervisord/conf.d/
```
Restart supervisord.


# UWSGI
The webserver that will run the app in a more robust multithreaded manner.
https://flask.palletsprojects.com/en/1.1.x/deploying/uwsgi/

