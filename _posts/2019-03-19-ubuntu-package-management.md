---
title: Ubuntu package management
tags:[linux, ubuntu, apt, apt-get, apt-cache, dpkg]
---

这本文章试图总结日常工作中用到的和软件包管理有关的命令。对这个问题，ubuntu有官方文档。

ubuntu软件包包含实现特定功能所必要的文件，元数据和指令。复杂的软件包还会包含依赖关系。软件包的日常管理主要分为：

1. 软件包仓库管理
1. 软件包管理

另外，本文也会附带介绍apt的底层工具dpkg和比较复杂的apt-get和apt-cache等。

## 软件包仓库管理
### 基本原理:
软件包仓库也就是包含软件包的服务器。但我们运行apt命令的时候， apt命令会到软件包仓库去搜索合适的软件包，以及其依赖的软件包。然后按次序安装。

apt通过读取特定的配置文件来获取软件仓库信息。默认情况下这个配置文件位于/etc/apt/sources.list 以及/etc/apt/sources.list.d/文件夹下所有扩展名为.list的文件。更详细的信息可以参考man source.list

用于配置apt的.list文件是个简单的文本文件。每一行代表一个软件包仓库. 具体格式如下:

```bash
# 毫无疑问，以#开头的是注释。
# 每一行包含以下部分，用空格分隔
# type: deb和deb-src, 其中deb表示软件包，deb-src表示源代码
# url: 软件包仓库的URL
# ubuntu release: ubuntu的版本名称
# components: 最后一部分是components. 可以有多个值，使用空格分隔
#             ubuntu常用的四个components为:main, universe, restricted和multiverse.
# 下面是两个例子
deb http://ch.archive.ubuntu.com/ubuntu/ saucy main restricted
deb-src http://ch.archive.ubuntu.com/ubuntu/ saucy main restricted
```

如果不知道自己的linux的发行版，可以通过lsb_release -sc来获取。

ubuntu的components的具体含义:

1. main: ubuntu官方支持的开源免费的软件包
1. universe: ubuntu社区支持的开源免费的软件包
1. restricted: 私有（专用）设备驱动
1. multiverse: 有版权或者存在法律争议的软件包

### 日常管理
日常管理中，很少会直接手动维护/etc/sources.list.d/下的.list文件。而是通过add-apt-repository命令来操作。

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:<repository-name>
sudo apt update
```
apt带有缓存，所以无论是手动修改文件还是通过add-apt-repository修改sources.list,最后都需要通过sudo apt update来更新软件仓库信息。

## 软件包管理
软件包的管理比较简单， 主要是使用apt命令。api命令的详细信息参考*man apt*. 基本用法如下:

```bash
# 安装软件之前，首先要做的就是apt update以获取软件产库的最新信息
sudo apt update
# 通过 install 命令安装软件包以及其依赖项
sudo apt install mysql
# 安装特定版本
sudo apt install mysql=5.7
# 安装特定发行版本
sudo apt install mysql/stable

# 通过 remove 命令卸载软件包 (不删除配置文件)
sudo apt remove mysql<br><br># 通过 purge 命令卸载软件包 (删除配置文件)<br>sudo apt purge mysql

# 通过show命令显示特定软包的信息
sudo apt show mysql

# 通过list命令显示可用软件包
sudo apt list

# 通过seach命令搜索特定软包
sudo apt search mysql
```
package 的名字除了可以指定版本号和发行版本之外，还可以带有+和-符号，带上+表示安装，-表示要删除。特别注意，在 apt remove 命令下， 如果软件包的名字带有+，apt 会执行安装而不是删除。

## dpkg, apt-get和apt-cache
dpkg是apt和apt-get的底层工具。dpkg的基本功能是安装本地.deb软件包。所以其不具有下载在线软件包的功能，也不可能去解决依赖包的问题。apt-get和apt-cache可以认为是apt的复杂版本。

dpkg的详细功能请参考 man dpkg 或者官方文档。相比于 apt, dpkg 有下面一些特殊功能

1. 安装本地.deb 软件包 dpkg -i xyz.deb
1. 查看安装包中包含哪些文件 dpkg -L xyz
1. 查看系统中某个文件来自于哪个软件包 dpkg -S /etc/host.conf

apt-get的详细功能请参考man apt-get。与之有关的还有 apt-cache 命令。正是由于 apt-get和 apt-cache 等命令使用起来较为复杂，才导致了 apt 命令的出现。apt 命令的维护者也在不断将 apt-get 和 apt-cache 的常用功能移入 apt。所以应该尽量使用 apt 命令。截止到写这边文章为止， apt-get 任然有以下功能没有移入 apt 命令：

1. 智能升级系统：sudo apt-get dist-upgrade
1. 只下载不安装：sudo apt-get download nginx

## 操作系统升级
操作系统升级可以通过sudo do-release-upgrade 来完成。当然，在升级之前至少应该先更新软件包仓库
```bash
# 更新软件包仓库信息
sudo apt update
# 检查是否存在新版本的系统
sudo do-release-upgrade -c
```