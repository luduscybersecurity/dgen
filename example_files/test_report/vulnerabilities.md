# Vulnerabilities

## Summary

| Description               | Rating                                | Status                    |
|:--------------------------|:--------------------------------------|:--------------------------|
| %{v_vuln_comps.name}      | [%{v_vuln_comps.rating}]{.rating}     | %{v_vuln_comps.status}    |
| %{v_csrf.name}            | [%{v_csrf.rating}]{.rating}           | %{v_csrf.status}          |
| %{v_cc_enc.name}          | [%{v_cc_enc.rating}]{.rating}         | %{v_cc_enc.status}        |
| %{v_dflt_pw.name}         | [%{v_dflt_pw.rating}]{.rating}        | %{v_dflt_pw.status}       |
| %{v_dom_privs.name}       | [%{v_dom_privs.rating}]{.rating}      | %{v_dom_privs.status}     |
| %{v_xmli.name}            | [%{v_xmli.rating}]{.rating}           | %{v_xmli.status}          |
| %{v_pass_sec_pol.name}    | [%{v_pass_sec_pol.rating}]{.rating}   | %{v_pass_sec_pol.status}  |
| %{v_sqli.name}            | [%{v_sqli.rating}]{.rating}           | %{v_sqli.status}          |
| %{v_xxe.name}             | [%{v_xxe.rating}]{.rating}            | %{v_xxe.status}           |
| %{v_miss_head.name}       | [%{v_miss_head.rating}]{.rating}      | %{v_miss_head.status}     |
| %{v_ip_whitelist.name}    | [%{v_ip_whitelist.rating}]{.rating}   | %{v_ip_whitelist.status}  |
| %{v_bus_log.name}         | [%{v_bus_log.rating}]{.rating}        | %{v_bus_log.status}       |
| %{v_serv_fp.name}         | [%{v_serv_fp.rating}]{.rating}        | %{v_serv_fp.status}       |

## Ratings

Vulnerabilities are rated on the urgency to fix based off a combination of the ease of exploit, impact if exploited and %{company}'s cyber security experience.

* [Urgent]{.urg}: The vulnerability is so severe it puts %{client} at an immediate unacceptable risk and should be fixed immediately.
* [High]{.high}: The vulnerability will likely put %{client} at an unacceptable risk, and should be fixed as quickly as practical.
* [Medium]{.med}: The vulnerability may become a serious threat to %{client}, especially if combined with another. It is recommended that the vulnerability be fixed as part of the next release/change window.
* [Low]{.low}: The vulnerability is not likely to become a serious threat to %{client}. It is recommended that the vulnerability be fixed as part of a future release as convenient.
* [Optional]{.opt}: The vulnerability is unlikely to pose even a low threat to %{client}, but has been included for the sake of completeness or because it is part of best practice. %{client} can use its discretion when deciding if to remediate.

Vulnerability statuses have been marked based on the results of retesting:

* **Fixed**: fixes for the vulnerability have been tested and confirmed effective.
* **Partial**: a partial or temporary fix has been put in place. A complete fix could not be implemented before completion of the engagement.
* **Untested**: the vulnerability could not be retested before the completion of the engagement.
