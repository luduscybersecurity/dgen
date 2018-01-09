---
v_dflt_pw:
    name: Missing/Default passwords
    rating: High
    num_treatments: '2'
    status: Untested
...

## %{v_dflt_pw.name}{.finding}

|Rating                          | Status             |
:--------------------------------|:-------------------|
|[%{v_dflt_pw.rating}]{.rating}  |%{v_dflt_pw.status} |

### Description

A number of hosts on the internal network were found with either default credentials or no passwords configured, granting access to information stored on the host.

The following hosts had either default or missing passwords:

* 10.3.11.11
* 10.3.11.12
* 10.3.11.13
* 10.3.11.14
* 10.3.11.16
* 10.3.11.17
* 10.3.11.18

The underlying accounts had clear-text credentials that were reused to compromise other hosts on the network including:

* The primary development server;
* An executive's email account; and
* A domain administrator account.

It was observed (but not tested), that compromise of these hosts could have been leveraged to compromise a Salesforce account with full privileges for BTB.

### Treatments
<div class="treatment">
#. Set passwords for all the hosts identified above for VNC and the "pi" account.
#. Set up service accounts when credentials must be saved to disk as part of a script, and ensure they have the minimum access required to fulfil their purpose.
</div>

BTB have stated that all Raspberry PIs have had their passwords changed and VNC passwords added. All scripts have been removed from the Raspberry PIs and logins for Salesforce use an account with minimum privileges.

### References

* [Test Raspberry PI devices](### Test Raspberry PI devices)
* [Pivot onto developer machine](### Pivot onto developer machine)
* [Pivot onto NAS server and achieve domain administrator privileges](### Pivot onto NAS server and achieve domain administrator privileges)
