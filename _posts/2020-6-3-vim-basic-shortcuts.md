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
1.  x: delete a char. this is a simple command
1.  d: delete. this is a start of deletion command expression. 
       for example, d3l means to delete 3 chars forward. d3b to delete 3 chars backward
1. dd: delete a line
1.  y: yank(copy) selection
1. yy: yank(copy) the current line

##search

##save & exit
1.  :w: write
1.  :q: quit
1. :q!: quit without saving
1. 
