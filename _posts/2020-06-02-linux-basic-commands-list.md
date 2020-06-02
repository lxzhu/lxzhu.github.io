---
title: Linux Basic Commands
tags: [Linux]
---

[GNU Coreutils](https://www.gnu.org/software/coreutils/manual/html_node/index.html){:target="blank"} is a better place to go.

Anyway this is my simple list

## man
1. man command is the command to show manual of other commands.

## file system

1. ls:      list directory contents. 
1. cd:      change current directory
1. pwd:     print working directory
1. touch:   create a new empty file
1. chmod:   change mode of file
1. chown:   change own of file
1. chgrp:   change group ownership
1. vim:     edit a file
1. rm:      remove a file
1. mv:      move a file; rename is a kind of move; move=cut+paste
1. cp:      copy a file
1. rsync:   pull file from remote host or push file to remote host
1. mkdir:   make a new dir
1. rmdir:   remove a dir
1. ln:      make a hard/symbolic link
1. fgetacl: get access control list of a file
1. fsetacl: set access control list of a file
1. basename: strip directory and suffix from a file name
1. dirname: strip last file name component

# file content manipulate
1. head: read head lines of a file
1. tail: read tail lines of a file
1. cat:  concatenate files
1. more: display file content in paging mode
1. less: display file content in paging mode and support move forward and backward.
1. cut:  print selected parts of lines
1. join: join lines on a common field
1. sort: sort lines of a file
1. uniq: remove adjacent duplicated lines of a file
1. wc: count word or line of a file
1. split: split files by lines, by size or by number of chunks
1. tr: translate, squeeze, and/or delete characters
1. tee: redirect output to multiple files or processes
1. base64: encode content to base64 or decode from base64 file
1. tar: archive files
1. gzip: compress a file 
1. gpg: encrypt a file

## administrator

1. getent: get entries of administrator database. for example, getent passwd get a list of users information
1. export: set environment
1. crontab: edit cron table file
## misc

1. echo: print text or environment variable
1. date: show date time
1. uname: print system information


## user info
1. who:

## logic
1. test: check file types and compare values
1. expr: evaluate expressions

# network

1. hostname: the hostname of current 
1. ifconfig: config network adapter
1. iwconfig: config wifi network adapter information
1. ping: ping a computer
1. traceroute: see how you connects to a server. for example: traceroute google.com
1. dig: domain information groper
1. nslookup: lookup dns information
1. host: find ip by host name or find host name by ip
1. netstat:  Netstat (Network Statistic) command display connection info, routing table information etc. [20 Netstat Command Examples in Linux.](https://www.tecmint.com/20-netstat-commands-for-linux-network-management/){:target="blank"}
1. arp: ARP (Address Resolution Protocol) is useful to view / add the contents of the kernel’s ARP tables.
1. telnet: connect to a remove server
1. ssh: ssh to remote server

