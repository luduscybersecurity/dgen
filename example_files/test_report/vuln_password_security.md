---
v_pass_sec_pol:
    name: Poor password security policy
    rating: Medium
    num_treatments: '3'
    status: Fixed
...

## %{v_pass_sec_pol.name}{.finding}

| Rating                              | Status                   |
|:------------------------------------|:-------------------------|
| [%{v_pass_sec_pol.rating}]{.rating} | %{v_pass_sec_pol.status} |

### Description

Several issues were discovered with password security:

* Passwords were not encrypted inside the application database. If the database is recovered by an adversary, they will have access to all users accounts, and may be able to reuse the passwords on other applications.
* While masked as a password field, the password was reflected back to the user in the "view user" feature, and could be recovered using developer tools or by viewing the page source. Someone who recovers a cached page or views another user's account will be able to compromise the user's account.
* A password complexity policy was not enforced. Setting a good password policy prevents users from choosing passwords that are easily guessable. OWASP recommends that complexity policies adhere to [NIST guidelines on password complexity](https://pages.nist.gov/800-63-3/sp800-63b.html#memsecret):
    * A minimum password length of 8.
    * Does not match common passwords, passwords obtained from previous breach corpuses, dictionary words, repetitive or sequential characters (e.g. ‘aaaaaa’, ‘1234abcd’), or context-specific words, such as the name of the service, the username, and derivatives thereof.
    * NIST recommend that the application should offer guidance to users when choosing a password, such as a password strength indicator.

%{company} understands that under certain circumstances it is necessary to store users passwords in a recoverable format (e.g. to assist in troubleshooting internet connections at an ISP). But such requirements should be carefully considered and limited to the minimum users required.

### Treatments
<div class="treatment">
#. Encrypt all passwords using a strong, scalable hashing algorithm such as PBKDF2, bcrypt or scrypt and use a unique salt for each credential.
#. Ensure that passwords are not included in responses when viewing user details.
#. Implement a password complexity policy that aligns with NIST recommendations.
</div>

BTB have hashed passwords using PBE with unique salts and a iteration count of 1000. Passwords are no longer reflected back to end users inside responses. A password complexity policy has been implemented which is 8 characters minimum, with at least 1 uppercase and 1 special character. Users are forced to change their password on login if the user has not changed their password for 3 months. BTB have provided code snippets as evidence.

### References

* [Examine user search/view/add features](## Examine user search/view/add features)
