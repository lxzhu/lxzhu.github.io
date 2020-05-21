---
title: Crash course to systemctl
subtitle: the least you should know about systemctl
tags: [linux, systemctl, service, daemon]
---

这篇文章的目的是列出 systemctl 的最常见的用法。更详细的信息可以通过man systemctl命令来查看。Linux 操作系统通过 init 进程来启动其它必要的进程。daemon 服务（类似于 windows 服务）就是作为 init 的子进程被启动的。

直接操作 init 脚本过于危险，所以更加面向用户的服务被发明出来。例如 upstart和 systemd. systemctl 命令可以认为是 systemd 的客户端。

## service 的日常管理
service 的日常管理，主要包括启动(start)，停止(stop)，重启(restart)，查看状态(status)，禁用(disable), 启动(enable)以及 mask和 unmask。其中比较令人费解的是 disable 和 mask 的差别。

当一个服务被 disable 之后，操作系统重启的时候不会自动启动它。 但是用户任然可以手动启动。当一个服务被 mask 之后，不仅操作系统不会自动启动它。用户也不能手动启动它。必须先进行 unmask 操作，然后才能 start.

```bash
# 以 nginx 为例说明服务的日常管理操作
# 列出系统中所有的服务
sudo systemctl list-units
# 列出系统中已经加载的服务
sudo systemctl list-units --state=loaded
# 列出所有的 socket
sudo systemctl list-sockets
# 列出所有的 timer
sudo systemctl list-timers
# 启动 nginx 服务
sudo systemctl start nginx
# 关闭 nginx 服务
sudo systemctl stop nginx
# 重启 nginx 服务
sudo systemctl restart nginx
# 查看 nginx 服务的状态
sudo systemctl status nginx
# 禁止 nginx 服务自动启动
sudo systemctl disable nginx
# 允许 nginx 服务自动启动
sudo systemctl enable nginx
# mask nginx 服务
sudo systemctl mask nginx
# unmask nginx 服务
sudo systemctl unmask nginx<br># 查看 nginx 服务日志<br>journalctl -u nginx
```

## 添加服务程序
直接编写daemon 程序需要用到 fork() 技术。具有一定的难度。借助 systemd 服务， 我们可以把任何一个控制台程序变成 daemon。

下面是 nginx.service 文件的内容。文件由三个部分构成：

1. Unit部分描述服务本身，以及这个服务与其他服务之间的依赖关系和启动次序关系。Unit 部分的完整属性列表请参考 man systemd.unit
1. Service部分主要是指定服务程序的类型，启动，停止和重启所对应的命令，以及启动之前的命令。Service 部分的完整属性列表请参考man systemd.service。在最简单的情况下，只需要有 ExecStart 一个属性即可。
1. Install 部分主要是和安装有关的属性。详细列表也在man systemd.unit。主要就是 Alias, WantedBy, RequiredBy 和 Also. 其中 Alias 用于给服务起别名。

```bash
[Unit]
Description=A high performance web server and a reverse proxy server
Documentation=man:nginx(8)
After=network.target

[Service]
Type=forking
PIDFile=/run/nginx.pid
ExecStartPre=/usr/sbin/nginx -t -q -g 'daemon on; master_process on;'
ExecStart=/usr/sbin/nginx -g 'daemon on; master_process on;'
ExecReload=/usr/sbin/nginx -g 'daemon on; master_process on;' -s reload
ExecStop=-/sbin/start-stop-daemon --quiet --stop --retry QUIT/5 --pidfile /run/nginx.pid
TimeoutStopSec=5
KillMode=mixed

[Install]
WantedBy=multi-user.target
```

service 文件写好(或者修改)之后，放置到/etc/systemd/system/目录下。然后通过 **sudo systemctl daemon-reload** 命令让 systemd 重新扫描 (读取)service文件。然后通过前面列举的命令对 service 进行控制。