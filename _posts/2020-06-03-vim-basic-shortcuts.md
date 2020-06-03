---
title: Vim Basic Shortcuts
tags: [vim]
---

## Switch mode
1. esc: Switch to command mode
1. i: Switch to insert mode

# move cursor in command mode

1.  $: to the end of the line
1.  ^: to the first non-blank character of the line
1.  e: to the end of the word. 
1. ne: to the end of the nth word. for example 3e.
1.  w: to the beginning of the word
1. nw: move forward n words. for example 3w.
1.  b: move backward a word
1. nb: move backward n words. for example 3b.
1.  j: jump forward one line
1. nj: jump forward n line. for example 3j
1.  G: jump to the end of the file
1. 1G: jump to the begining of the file. the same as gg
1. gg: jump to the begining of the file. the same as 1G
1. ``: two backticks, return to the cursor position before the latest jump (undo the jump)
1. mx: set mark x at current cursor. the mark name x must be single character
1. `x: jump to mark x
1. 'x: jump to the beginning of the line of the mark x
1. g;: jump to the place of last edit
1.  %: jump to matched brace.

## cut, delete, copy & paste
| command | explaination |
|---|---|
|x|delete a char|
|d|delete. this is a start of delete command expression. in a command expression, you need to specify command, number, direction with unit. for example,  d3l means delete three chars forward; d3h means to delete three chars backward;  d2j delete 2 lines forward; d3k means to delete three lines back;|
|dd|delete current line|
|y| yank(copy) command starts|
|yy| yank(copy) current line|
|p| paste after current cursor|
|P| paste before the current cursor|


##search

##save & exit
1.  :w: write
1.  :q: quit
1. :q!: quit without saving
1. 
