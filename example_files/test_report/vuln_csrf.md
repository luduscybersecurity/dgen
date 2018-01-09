---
v_csrf:
    name: Application vulnerable to Cross Site Request Forgery
    rating: Urgent
    num_treatments: '1'
    status: Fixed
...

## %{v_csrf.name}{.finding}

| Rating                      | Status           |
|:----------------------------|:-----------------|
| [%{v_csrf.rating}]{.rating} | %{v_csrf.status} |

### Description

The application is vulnerable to Cross Site Request Forgery (CSRF), which was exploited to create 'admin' level accounts. 

CSRF is an attack that tricks the victim into submitting a malicious request. It inherits the identity and privileges of the victim to perform an undesired function on the attacker's behalf. For most sites, browser requests automatically include any credentials associated with the site, such as the user's session cookie, IP address, and Windows domain credentials. Therefore, if the user is currently authenticated to the site, the site will have no way to distinguish between the forged request sent by the victim and a legitimate request sent by the victim.

OWASP makes several suggestions in regards to preventing CSRF that all come with engineering trade-offs:

* Checking Referrer headers: This can be an effective control when implemented correctly. However there are a number of potential draw-backs to this solution:
    * It relies on the presence of a referrer header, which may conflict with privacy requirements and applications that have cross origin functionality.
    * It relies on the browser to attach the referrer header correctly. Vulnerabilities have been found in browsers over time where an attacking site can manipulate the vulnerable browser into setting an incorrect referrer.
* The synchroniser token values relies on all operations being implemented as POSTs, and consumes additional memory as the synchroniser token must be stored server side with the user's session.
* While an elegant solution, the double submit cookie pattern does not work well for applications that make use of cross origin requests (e.g. a user interface hosted on one origin and applicaiton APIs hosted on another).
* The encrypted token pattern relies on the selection of a suitable encryption algorithm, may be vulernable to a padding oracle attack and should have the nonce written first in the encryption string to make collision attacks more difficult.

### Treatments
<div class="treatment">
#. Select one of the CSRF defences and apply it to all functionality that results in a server side state change.
</div>

BTB have implemented referrer checking, which has been confirmed effective by %{company}.

### References

* [Exploit CSRF to gain access](### Exploit CSRF to gain access)
