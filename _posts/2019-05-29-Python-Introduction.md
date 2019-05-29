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