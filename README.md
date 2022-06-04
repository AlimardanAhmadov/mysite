# Apache Webserver Configuration

sudo nano /etc/apache2/sites-available/mysite.conf or sudo nano /etc/apache2/mysite.conf

<VirtualHost *:80>
	ServerAdmin admin@mysite.localhost
	ServerName mysite.localhost
	ServerAlias www.mysite.localhost
	DocumentRoot /home/al1mardan/mysite
	ErrorLog ${APACHE_LOG_DIR}/error.log
	CustomLog ${APACHE_LOG_DIR}/access.log combined

	Alias /static /home/user/mysite/static
	<Directory /home/al1mardan/mysite/static>
		Require all granted
	</Directory>

	Alias /static /home/al1mardan/mysite/media
	<Directory /home/al1mardan/mysite/media>
		Require all granted
	</Directory>

	<Directory /home/al1mardan/mysite/mysite>
		<Files wsgi.py>
			Require all granted
		</Files>
	</Directory>

	WSGIDaemonProcess django_project python-path=/home/user/django_project python-home=/home/user/django_project/env
	WSGIProcessGroup django_project
	WSGIScriptAlias / /home/al1mardan/mysite/mysite/wsgi.py
</VirtualHost>


# AWS EC2

SECURITY GROUPS:
security-group-django-linux-server

RDS:
Database server: PostgreSQL-djangoserver
User: tugayadmin
Password:  tugay2022

EC2:
Public IP address: 3.95.212.120