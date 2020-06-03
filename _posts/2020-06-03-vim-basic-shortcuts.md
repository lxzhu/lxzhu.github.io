---
title: Vim Basic Shortcuts
subtitle: move cursor in file and search, cut, copy, paste, delete etc
tags: [vim]
---

## Switch between command mode and editing mode

| command | explanation |
| ------: | ------ |
| esc| Switch to command mode |
| i  | Switch to insert mode |

# move cursor in command mode

| command | explanation |
| ------: | ------ |
|  $ | to the end of the line|
|  ^ | to the first non-blank character of the line |
|  e | to the end of the word. |
| ne | to the end of the nth word. for example 3e. |
|  w | to the beginning of the word |
| nw | move forward n words. for example 3w. |
|  b | move backward a word |
| nb | move backward n words. for example 3b. |
|  j | jump forward one line  |
| nj | jump forward n line. for example 3j  |
|  G | jump to the end of the file  |
| 1G | jump to the begining of the file. the same as gg  |
| gg | jump to the begining of the file. the same as 1G  |
| `` | two backticks, return to the cursor position before the latest jump (undo the jump) |
| mx | set mark x at current cursor. the mark name x must be single character |
| `x | jump to mark x |
| 'x | jump to the beginning of the line of the mark x |
| g; | jump to the place of last edit |
|  % | jump to matched brace. |

## cut, delete, copy & paste

| command | explanation |
| ------: | ------ |
| x |delete a char|
| d |delete. this is a start of delete command expression. in a command expression, you need to specify command, number, direction with unit. for example,  d3l means delete three chars forward; d3h means to delete three chars backward;  d2j delete 2 lines forward; d3k means to delete three lines back;|
| dd |delete current line|
| y | yank(copy) command starts|
| yy| yank(copy) current line|
| p | paste after current cursor|
| P | paste before the current cursor|


##search

##save & exit

| command | explanation |
| ------: | ------ |
|  :w| write |
|  :q| quit |
| :q!| quit without saving |
|:w !sudo tee %| save editing with sudo permission. this is used when you forget to start vim with sudo. </br>:w write the conent to the buffer, ! starts a shell command. and tee write content from buffer to file; % is the current file name. so the command is  write content to buffer and then run sudo tee {current file name} in a shell to write buffer into file.|

