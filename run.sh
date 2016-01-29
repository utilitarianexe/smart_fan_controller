export PYTHONPATH="${PYTHONPATH}:/home/pi/smart_fan/"
echo "hi" >> /home/pi/smart_fan/please
#python become_access_point.py
/usr/local/bin/uwsgi  --catch-exceptions  --chdir /home/pi/smart_fan/ --ini  /home/pi/smart_fan/smartfan.ini
echo "the end" >> /home/pi/smart_fan/please
