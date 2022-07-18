# VulnApp Demonstration
This application contains a CSRF vulnerability that allows an attacker to trick an existing admin to toggle the "admin" boolean for an existing user.

## TODO
Create a micro-blog to exploit the stored XSS to make this problem worse such that any user send an admin a ticket and the ticket stores the XSS used to exploit the vulnerability