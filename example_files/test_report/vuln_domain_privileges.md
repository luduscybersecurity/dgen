---
v_dom_privs:
    name: Domain Privileges
    rating: High
    num_treatments: '3'
    status: Untested
...

## %{v_dom_privs.name}{.finding}

| Rating                           | Status                |
:----------------------------------|:----------------------|
| [%{v_dom_privs.rating}]{.rating} | %{v_dom_privs.status} | 

### Description

A number of issues were found with the members of the domain admins group increasing the ease with which the domain could be compromised.

An image of the members of domain admins is below:

![domain_administrators.png](images/list_of_domain_admins.png "List of Domain Admins")

The issues are:

* Domain admin accounts had been granted to people's everyday use accounts. If compromised, for example as part of a spear phishing campaign, the entire domain would be instantly compromised.
* A number of service accounts had been granted domain administrator privileges. This is almost never necessary as the accounts will often only need to run on a small number of servers.
* A generic domain account, b2badmin, that is shared by other members of the organisation was identified. This reduces accountability within the domain should the account be used for malicious purposes. 

### Treatments
<div class="treatment">
#. Set up separate accounts for domain administration and everyday use.
#. Rationalise service accounts so they have least privilege.
#. Eliminate all shared accounts
</div>

### References

* [Pivot onto NAS server and achieve domain administrator privileges](### Pivot onto NAS server and achieve domain administrator privileges)
* [Achieve domain dominance](### Achieve domain dominance)
