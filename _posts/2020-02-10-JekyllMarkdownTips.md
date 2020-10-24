---
layout: post
title: Jekyll Markdown Tips
subtitle: a list of examples
tags: [markdown, MathJax]
ext-js:
  - https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.29.1/moment.min.js
---

You can write regular [markdown](http://markdowntutorial.com/) here and Jekyll will automatically convert it to a nice webpage.  I strongly encourage you to [take 5 minutes to learn how to write in markdown](http://markdowntutorial.com/) - it'll teach you how to transform regular text into bold/italics/headings/tables/etc.

**Here is some bold text**

## Here is a secondary heading

Here's a useless table:

| Number | Next number | Previous number |
| :------ |:--- | :--- |
| Five | Six | Four |
| Ten | Eleven | Nine |
| Seven | Eight | Six |
| Two | Three | One |


How about a yummy crepe?

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg)

Here's a code chunk:

~~~
var foo = function(x) {
  return(x + 5);
}
foo(3)
~~~

And here is the same code with syntax highlighting:

```javascript
var foo = function(x) {
  return(x + 5);
}
foo(3)
```

And here is the same code yet again but with line numbers:

{% highlight javascript linenos %}
var foo = function(x) {
  return(x + 5);
}
foo(3)
{% endhighlight %}

## Boxes
You can add notification, warning and error boxes like this:

### Notification

{: .box-note}
**Note:** This is a notification box.

### Warning

{: .box-warning}
**Warning:** This is a warning box.

### Error

{: .box-error}
**Error:** This is an error box.


### MathJax 

When $$a \ne 0$$, there are two solutions to $$(ax^2 + bx + c = 0)$$ and they are
$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}.$$

### Customized JavaScript
1. add into layout file for js shared
1. add into page.ext-js for js from external site
1. add into page.js for js inside your github repo

For example, in this post, i can use moment.js. 
<div>Current moment is:<span id="now"/></div>
  
<script>
  $(document).ready(function(){
     $("#now").text(moment().format('MMMM Do YYYY, h:mm:ss a'));
  }); 
</script>

