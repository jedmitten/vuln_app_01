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