
---
ssrxss:
    name: Server Side Reflected Cross Site Scripting
    class: 
        - XSS
        - Session Weakness
    rating: Medium
    impact: High
    likelihood: Medium
    summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at nisl sollicitudin, fermentum erat in, tristique nunc.
...

# %{ssrxss.name}{.finding}
  Rating                        | Impact            | Likelihood
  :-----------------------------|:------------------|:------------
  [%{ssrxss.rating}]{.rating}   | %{ssrxss.impact}  | %{ssrxss.likelihood}

## Finding Details

%{ssrxss.summary}

Some text goes here.

## Treatments
<div class="treatment">
#. Recomendation 1
#. Recomendation 2 
</div>
