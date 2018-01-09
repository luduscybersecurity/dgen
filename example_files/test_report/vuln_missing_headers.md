---
v_miss_head:
    name: Missing HTTP headers
    rating: Low
    num_treatments: '1'
    status: Fixed
...

## %{v_miss_head.name}{.finding}

| Rating                           | Status                |
|:---------------------------------|:----------------------|
| [%{v_miss_head.rating}]{.rating} | %{v_miss_head.status} |

### Description

The application does not set HTTP headers according to security best practice. 

Missing headers, recommended settings and their purposes are detailed below.

  * **X-Frame-Options: DENY** - 
  X-Frame-Options prevents a third party website from including this website within an iFrame. This can lead to a number of attacks including ClickJacking (or a "UI redress attack"), which is where an attacker uses multiple transparent or opaque layers to trick a user into clicking on a button or link on another page when they were intending to click on the the top level page. Thus, the attacker is "hijacking" clicks meant for their page and routing them to another page, most likely owned by another application, domain, or both. Click-jacking attacks can also be used to log keystrokes and steal passwords. Further information on possible values for X-Frame-Options can be found at https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options.
  * **Cache-control: no-store** and **Pragma: no-cache** - 
  These headers direct browsers not to cache the page. If an attacker is able to later access a users workstation, they may be able to recover sensitive data from the application.
  * **Strict-Transport-Security: max-age=31536000; includeSubDomains** - 
  HTTP Strict Transport Security directs the browser that the page should always be encrypted (i.e. to request the encrypted resource) and to apply strict certificate validation. This prevents three threats:
    #. User bookmarks or manually types http://example.com and is subject to a man-in-the-middle attacker. HSTS automatically redirects HTTP requests to HTTPS for the target domain.
    #. Web application that is intended to be purely HTTPS inadvertently contains HTTP links or serves content over HTTP. HSTS automatically redirects HTTP requests to HTTPS for the target domain.
    #. A man-in-the-middle attacker attempts to intercept traffic from a victim user using an invalid certificate and hopes the user will accept the bad certificate. HSTS does not allow a user to override the invalid certificate message.
  The max-age directive tells the browser how many seconds it should cache the HSTS rule, with the recommended value being 1 year. The includeSubDomains directive tells the browser that the rule should be applied to all sub-domains of the application.
  * __Content-Security-Policy: default-src 'self' *.trusted.com__ - 
  Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement or distribution of malware. The example setting allows content to be loaded from the origin domain and all sub-domains of trusted.com. Configuring content security policy can be a complicated exercise, especially where the site uses content from a number of different sources (especially those that are user defined). https://developers.google.com/web/fundamentals/security/csp/ provides more information on how to configure CSP, and a tool such as https://oxdef.info/csp-tester/ can assist in generating a functional policy.
  * **X-XSS-Protection: 1; mode=block** - 
  The HTTP X-XSS-Protection response header is a feature of Internet Explorer, Chrome and Safari that stops pages from loading when they detect reflected cross-site scripting (XSS) attacks. Although these protections are largely unnecessary in modern browsers when sites implement a strong Content-Security-Policy that disables the use of inline JavaScript ('unsafe-inline'), they can still provide protections for users of older web browsers that don't yet support CSP. The example value directs the browser to detect reflected XSS attacks and prevent the page from loading if one is discovered. If CSP has been properly configured, setting the header value to "X-XSS-Protection: 0" will not result in a degradation in security and prevent any rendering errors caused by bugs in the browser's XSS protection filter.
  * **X-Content-Type-Options: nosniff** - 
  X-Content-Type-Options is a marker used by the server to indicate that the MIME types advertised in the Content-Type headers should not be changed and be followed. This allows to opt-out of MIME type sniffing, where a browser would attempt to detect a resource's MIME type based on its content. This setting will prevent scenarios where content sniffing could transform non-executable MIME types into executable MIME types.
  * **Referrer-Policy: same-origin** - 
  The referrer-policy header directs the browser only to include a referrer header (stating the resource that generated the current request) under certain conditions. This can be useful to protect an user's privacy from cross domain refferer leakage, but may break analytics platforms. In the example value a referrer will be sent for same-site origins, but cross-origin requests will contain no referrer information. Further information about valid directives can be found at https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy.

### Treatments
<div class="treatment">
#. Set each of the HTTP headers as recommended above.
</div>

BTB have set the headers as recommended and provided configuration files as evidence.

### References

* [Application reconnaissance](### Application reconnaissance) 
* [Examine authentication and session management](### Examine authentication and session management)
