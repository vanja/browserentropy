# Web Browser Entropy

This is an extendible framework for measuring the entropy of web browser fingerprints, developed as 
part of a research project on browser fingerprinting at the Vienna University of Technology. 
The framework uses third-party JS libraries for fingerprinting purposes (Fingerprint2.js, Modernizr, etc.).

# Demo
https://fingerprint.sba-research.org/

# Requirements

* **Python** (tested with 2.7.10)
* **Bottle**
* **MongoDB**
* **PyMongo**

# Usage

1) Start MongoDB server (default is ```localhost:27017```).

2) Run ```app.py```, edit hostname and port if necessary (default is ```localhost:8080```).

2a) In order for SSL/TLS handshake analysis to work, the framework needs to be deployed on Apache HTTP Server 
with running ```mod_ssl``` and ```sslhaf``` modules.

## Apache configuration

Here is an excerpt from the Apache config:
```
WSGIDaemonProcess BrowserEntropy python-path=<virtenv-path>/lib/python2.7/site-packages
WSGIScriptAlias / <path>/app.wsgi
<Directory <path>>
	WSGIProcessGroup BrowserEntropy
	WSGIApplicationGroup %{GLOBAL}
	Require all granted
</Directory>
```
where ```<path>``` and ```<virtenv-path>``` are project root directory and virtenv root directory, respectively, 
and ```app.wsgi``` is a symbolic link to ```app.py```.

Also, make sure to define a custom HTTP header to forward SSL/TLS handshake fingerprint data which can then be
parsed in Bottle web framework:
```
RequestHeader add X-Custom-Header-CipherSuites "\"%{SSLHAF_HANDSHAKE}e\" \
\"%{SSLHAF_PROTOCOL}e\" \"%{SSLHAF_SUITES}e\" \"%{SSLHAF_COMPRESSION}e\" \
\"%{SSLHAF_EXTENSIONS}e\" \"%{User-Agent}i\""
```

## License
[MIT License](https://opensource.org/licenses/MIT)
