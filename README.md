# VulnApp Demonstration

## Selected Vulnerability
This application contains a CSRF (cross-site request forgery) vulnerability that allows an attacker to trick an existing admin to toggle the "admin" boolean for an existing user. While there are actually other CSRF exploits an attacker can take advantage of in this example code, that is the case I am concentrating on.


## Description of Vulnerability
* CSRF is an attack that forces an authenticated application user to perform an unauthorized action on behalf of an attacker
* The vulnerability is present when an application does not validate that the authenticated user is intending to perform an action. A common form of CSRF exploits is forcing an administrator to modify an existing user or create a new one with administrative capabilities.
* Once the attacker builds an exploit in HTML or JavaScript, a successful XSS or phishing attack can get an administrator to visit the malicious URL, exploit the vulnerability, and have the application perform the action described in the exploit.

## The Vulnerability In-Use
* In 2020, reports of a vulnerability in TikTok described a series of events that allowed attackers to submit requests to the TikTok application through victim accounts. 
* In 2014, McAfee Network Security Manager had a vulnerability that allowed attackers to modify user accounts through a CSRF attack against administrators.

## Vulnerability Illustration
As an example, a vulnerable banking application may allow a user to transfer money from one account to another. Assuming the attacker knows their own account name (below it's `MARIA`), this simple example shows that an unwary administrator may click "View my pictures" and accidentally transfer money to the MARIA account.

```html
...
<form action="http://bank.com/transfer.do" method="POST">

<input type="hidden" name="acct" value="MARIA"/>
<input type="hidden" name="amount" value="100000"/>
<input type="submit" value="View my pictures"/>

</form>
...
```

The form can also autmatically be submitted using javascript such as

```html
<body onload="document.forms[0].submit()">
```

## Vulnerability Remediation
* Adding a server-controlled nonce (unique value that changes with every refresh) to the URL throughout the web application effectively prevents CSRF
* For example, whenever a user transitions to a new page, the server will assign a nonce value (such as a long integer) that ensure the user is clicking on the page and not being exploited.
* Modern browsers prevent some JavaScript exploits of CSRF through same-origin policy restrictions. Unless the application server allows cross-origin requests from the attacker's server, the CORS restrictions will block an attack such as
```html
<script>
function put() {
    var x = new XMLHttpRequest();
    x.open("PUT","http://bank.com/transfer.do",true);
    x.setRequestHeader("Content-Type", "application/json");
    x.send(JSON.stringify({"acct":"BOB", "amount":100})); 
}
</script>

<body onload="put()">
```

# Vulnerable App Usage
* In this example code, the form is vulnerable to CSRF by default. The application is written with `flask`, a python framework for quick web and API development. 

https://github.com/jedmitten/vuln_app_01/blob/main/project/__init__.py#L6-L7
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin

### VULNERABLE VERSION ###
from flask_admin.contrib.sqla import ModelView
```

By default, there is no security around form submissions that are automatically generated using `flask-admin` `ModelView` objects. The `ModelView` object takes a separate class and presents a view to create, read, update, or delete instances of the class (for example, Users)

Using the simple `ModelView` does not include security as found in https://github.com/jedmitten/vuln_app_01/blob/main/project/__init__.py#L45-L46

```python
    admin.add_view(ModelView(User, db.session))
```

You can see the User class at https://github.com/jedmitten/vuln_app_01/blob/main/project/models.py

`flask-admin` provides the functionality to add CSRF protection to forms using a `SecureForm` feature. See https://github.com/jedmitten/vuln_app_01/blob/main/project/views.py for the implementation. This creates a new model view called `SecureModelView` that implements the `SecureForm` when used.

By updating `__init__.py` to import the `SecureModelView`
```python
from .views import SecureModelView
```

and then utilize that class
```python
    admin.add_view(SecureModelView(User, db.session))
```

CSRF protection is added to the User admin form


# Running the Application
1. Clone the repository
1. From the repository directory, run `bash init.sh` to initalize the project (requires `python3`)
1. Run `bash run.sh` to run the application. Then navigate to `http://127.0.0.1:/5000` with a browser
1. There are 2 users setup during initialization
   1. Admin: username: admin@example.com, password: adminpassword
   1. Alice: username: alice@examplecom, password: monkey1
