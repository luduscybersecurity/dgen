---
v_bus_log:
    name: Business Logic Error
    rating: Optional
    num_treatments: '1'
    status: Untested
...

## %{v_bus_log.name}{.finding}

| Rating                         | Status              |
|:-------------------------------|:--------------------|
| [%{v_bus_log.rating}]{.rating} | %{v_bus_log.status} |

### Description

The application did not perform business logic checks to ensure that sell price inc GST is equal to sell price ex GST + 10%. It was possible to enter any value into either field without consideration for the other. For example the application would accept the following input:

| Sell Price | Sell Price + GST |
|:----------:|:----------------:|
| $200       | $5               |

### Treatments
<div class="treatment">
#. Modify application logic to auto populate Sell Price + GST based off the Sell Price.
</div>

### References

* [Application reconnaissance](### Application reconnaissance)
