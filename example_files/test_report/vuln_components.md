---
v_vuln_comps:
    name: Vulnerable libraries in use
    rating: Urgent
    num_treatments: '3'
    status: Partial
...

## %{v_vuln_comps.name}{.finding}

| Rating                                   | Status                 |
|:-----------------------------------------|:-----------------------|
| [%{v_vuln_comps.rating}]{.rating} | %{v_vuln_comps.status} |

### Description

A number of vulnerable components were identified in the application. One was exploited to get unauthenticated remote code execution on the server.

The version of struts in use (1.2.9) allowed for remote code execution via a vulnerabiliy which allowed %{company} to modify the classloader. Specifically, the logfile location was changed to a publicly accessible directory, the extension reset to .jsp, and the log format changed to facilitate injection of JSP code via the user-agent string.

It is noted that the version of struts in use is no longer supported by the developer.

A scan of the libraries using OWASP Dependency Check identified a total of 419 vulnerabilities across 9 dependencies, with the following having a high severity:

  * commons-beanutils-1.7.0.jar
  * commons-collections-3.1.jar
  * commons-fileupload-1.0.jar
  * mysql-connector-java-5.1.7-bin.jar
  * spring-core-4.1.6.RELEASE.jar
  * standard.jar
  * struts-1.2.9.jar

### Treatments
<div class="treatment">
#. Integrate the classloader filter located at https://github.com/rgielen/struts1filter
#. Upgrade the identified libraries to their latest versions.
#. Upgrade struts to version 2 of the framework.
</div>

BTB have implemented the classloader filter as suggested, which has been confirmed effective by %{company}. A migration from struts to spring is planned for a future release.

### References

* [Test for struts 1 classloader vulnerability](### Test for struts 1 classloader vulnerability)
* [Post exploitation of struts 1 classloader](### Post exploitation of struts 1 classloader)
* [Libraries in use](#### Libraries in use)
