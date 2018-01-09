---
v_ip_whitelist:
    name: IP whitelisting not in place as stated
    rating: Optional
    num_treatments: '1'
    status: Untested
...

## %{v_ip_whitelist.name}{.finding}

Rating                          | Status               |
:-------------------------------|:---------------------|
[%{v_ip_whitelist.rating}]{.rating} | %{v_ip_whitelist.status} | 

### Description

White-listing of IP addresses for CINDY did not appear to be in place as stated.

Scans of the Internet facing infrastructure identified the two CINDY production instances located at  103.74.184.248 and 103.55.76.23. Testing from a second IP using a VPN gave the same result. 

Further tests for application level access controls were not performed as login credentials had not been provided, and exploitation of the application via the vulnerability [%{v_vuln_comps.name}](## %{v_vuln_comps.name}) was deemed too risky.

### Treatments
<div class="treatment">
#. Limit access to the application via a firewall.
</div>

### References

* [Scan external infrastructure](### Scan external infrastructure)
