---
v_template:
    name: Vulnerability template finding
    rating: Medium
    num_treatments: '1'
    status: Untested
...

## %{v_template.name}{.finding}

Rating                          | Status               |
:-------------------------------|:---------------------|
[%{v_template.rating}]{.rating} | %{v_template.status} | 

### Description

Description of vulnerability. Must include:

* Summary of vulnerability and impact.
* Complete steps to replicate including exploitation.
* Where the vulnerability is simple enough/exploitation isn't practical, a description of the problem is with examples is sufficient.
* Screen-shots/code samples as practical.

### Treatments
<div class="treatment">
#. Recommendation 1
#. Recommendation 2 
</div>

### References

* Reference 1
