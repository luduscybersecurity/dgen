
---
%{file}:
    name: Insecure HTTP Headers
    class:
        - System Configuration
    rating: Low
    impact: Low
    likelihood: Medium
    summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at nisl sollicitudin, fermentum erat in, tristique nunc. Nulla in tortor quam. Vestibulum malesuada quam sit amet accumsan efficitur. 
...

# %{%{file}.name}{.finding}
  Rating                        | Impact              | Likelihood
:-------------------------------|:--------------------|:------------
  [%{%{file}.rating}]{.rating} | %{%{file}.impact}  | %{%{file}.likelihood}

## Finding Details

%{%{file}.summary}

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at nisl sollicitudin, fermentum erat in, tristique nunc. Nulla in tortor quam. Vestibulum malesuada quam sit amet accumsan efficitur. Aliquam maximus, erat sed mollis pharetra, leo dolor scelerisque dui, a ornare mauris eros vel sapien. Etiam id risus ligula. Sed vitae consequat justo. Sed ornare erat in mauris placerat, pharetra porttitor nibh ornare. Morbi porta feugiat libero, eu auctor ex malesuada sit amet. Aenean lobortis lectus et eros pellentesque aliquet.

~~~~ {#mycode .c .numberLines startFrom="100"}
void main(char** args, int argc)
{
    return 1;
}
another function(char** array)
{
    return void
}

more code goes here
wwwwwwwwwwwwwwwwwww
iiiiiiiiiiiiiiiiiii
~~~~

- list1
- list2
    #. list3
    #. list4

some more text not in a list

-list 1
-list 2
    some text for list 2

![an image caption](image.png)

blah blah blah. there will be a link just here: <http://www.google.com>

blah blah blah another link [here](http://www.google.com).

> this is a block quote
and the quote has been continued

> > block within a block
block wihtin block continued

Here is an inline note.^[Inlines notes are easier to write, since
you don't have to pick an identifier and move down to type the
note.]

Super/subscript: H~2~O is a liquid.  2^10^ is 1024.

<div class="clrtbl">
  Col1     |Col2    |Col3
-----------|--------|-------------
  Val1     |Val2    |Val3

Table: a table caption 
</div>

## Treatments
<div class="rec">
#. Recomendation 1
#. Recomendation 2 
</div>
