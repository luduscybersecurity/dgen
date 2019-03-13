
---
%{file}:
    name: Server Side Reflected Cross Site Scripting
    class: 
        - XSS
        - Session Weakness
    rating: Medium
    impact: High
    likelihood: Medium
    summary: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent at nisl sollicitudin, fermentum erat in, tristique nunc.

...

# %{%{file}.name}{.finding}
  Rating                        | Impact            | Likelihood
  :-----------------------------|:------------------|:------------
  [%{%{file}.rating}]{.rating}   | %{%{file}.impact}  | %{%{file}.likelihood}

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

- list 1
- list 2
    some text for list 2

![an image caption](screenshot.jpg)

blah blah blah. there will be a link just here: <https://microsoft.com>

blah blah blah. there will be a link just here: <%{var1}>

blah blah blah another link [%{var1}](%{var1}).

%pagebreak

> this is a block quote
and the quote has been continued

> > block within a block
block wihtin block continued

Here is an inline note.^[Inlines notes are easier to write, since
you don't have to pick an identifier and move down to type the
note.]

Super/subscript: H~2~O is a liquid.  2^10^ is 1024.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?

At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.

<div class="clrtbl">
  Col1     |Col2    |Col3
-----------|--------|-------------
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3
  Val1     |Val2    |Val3

Table: a table caption 
</div>

## Treatments
<div class="treatment">
#. Recomendation 1
#. Recomendation 2 
</div>
