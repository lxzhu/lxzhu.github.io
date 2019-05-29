---
layout: post
title: Python Introduction
subtitle: To get the point of python
tags: [python]
---

Maybe [Python official website](https://www.python.org/) is a better place to go.

## Basic Profile
Python is an mature cross platform, weak type, interpreted language. It is also supported to be compiled into modules to save loading and execution time.

Here is an example to demo python's basic syntax:

```python
# # starts a comment

# the parameter has no type
def bubble(nums):
    # there is no Parentheses
    # there is not curly bracket (brace)
    # indentation make this for statement a part of bubble function
    for i in range(len(nums)):
        for j in range(i+1,len(nums)):
            if nums[i]>nums[j]:
                # a nice way to swap values
                nums[j],nums[i]=nums[i],nums[j]

# not need any leading word to declare a variable
nums=[8,5,6,4,1,2,3]
# f-string is how string interpolation works in python
print(f"before sorting:{nums}")
bubble(nums)
print(f"after sorting:{nums}")
```

## Bulit-in Types
Builtin-in types are types that along with the interpreter. 
Here are most used python types:

1. boolean: __True__ or __False__
1. int
1. float
1. complex: complex concept in math. a+bi
1. list: a mutable sequence. 
1. tuple: a immutable sequence.
1. range:
1. str: a sequence of characters
1. set: 
1. dict: dictionary, hash table.

Key(special) points:

__boolean__: a boolean variable is either __True__ or __False__. However, __None__, __0__, __0.0__ and empty sequences(__''__, __()__, __[]__, __set()__ and __range(0)__) are __False__ in logical expression. __and__, __or__ and __not__ are used to connect logicial expression.

__common sequence operations:__
assume _s_ and _t_ are sequences and _x_ is the same type as element in _s_
| operation | description |
|---|---|
|x in s             | |
|x not in s         | |
|s+t                | concatenation of s and t|
|s*n                | add s to itself n times|
|s[i]               | read the ith element |
|s[i:j]             | slice s from i to j|
|s[i:j:k]           | slice s from i to j with step k|
|len(s)             | |
|min(s)             | |
|max(s)             | |
|s.index(x,[i,[j]]) | index of x between i and j|
|s.count(x)         | occurances of x in s| 

__list__:
1. to add an element to the end: __append__
2. to add an list of elements to the end: __extend__
3. to remove a value: __remove__
4. to remove a value at specific index: __pop__
5. to insert a value: __insert__
6. to clear a list: __clear__
7. to make a copy: __copy__
8. to reverse a list : __reverse__
9. to sort a list: __sort__. __sort__ supports to specify key function to get key for each element.

__str__:

First of all, __str__ is a sequence so _common sequence operations_ works for __str__.

[String Methods](https://docs.python.org/3.7/library/stdtypes.html#string-methods) has a list of methods. Here is an abridged list.

1. isspace:
1. 