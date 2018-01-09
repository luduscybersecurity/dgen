---
v_serv_fp:
    name: Application infrastructure can be fingerprinted
    rating: Optional
    num_treatments: '2'
    status: Fixed
...

## %{v_serv_fp.name}{.finding}

| Rating                         | Status              |
|:-------------------------------|:--------------------|
| [%{v_serv_fp.rating}]{.rating} | %{v_serv_fp.status} |

### Description

It was possible to fingerprint the application infrastructure. While not a vulnerability in itself, server fingerprinting can be useful when targeting further attacks against the applications infrastructure. For example, in targeting the frameworks and components that make up the application.

While essentially a strategy of security through obscurity, making it more difficult to target a server will hamper such attacks.

### Treatments
<div class="treatment">
#. Replace default error pages with a generic page that does not identify the hosting platform nor disclose any information that may be used to infer the cause of the error (such as stake traces).
#. Strip page extensions to obfuscate the presentation frameworks in use.
</div>

BTB state that they have modified the Tomcat configuration as recommended.

### References

 * [Application reconnaissance](### Application reconnaissance)
