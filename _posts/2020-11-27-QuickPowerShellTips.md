---
title: Quick PowerShell Tips
tags: [PowerShell, Test-Path,Get-Item,Get-ChildItem,Get-Content,Remove-Item, Select-Object, Sort-Object, ForEach, Get-Member, $_, $PSVersionTable] 
---

This post contains some basic information about PowerShell. For example: How to get the version of the powershell environment? 
What modules are installed? What commands are available? How to manipulate file system? etc.

## $PSVersionTable

*$PSVersionTable* is a global PowerShell Object. So you just type $PSVersionTable, the shell will print the information. Here is an example

```powershell
PS C:\Users\lxzhu> $PSVersionTable

Name                           Value
----                           -----
PSVersion                      5.1.18362.1171
PSEdition                      Desktop
PSCompatibleVersions           {1.0, 2.0, 3.0, 4.0...}
BuildVersion                   10.0.18362.1171
CLRVersion                     4.0.30319.42000
WSManStackVersion              3.0
PSRemotingProtocolVersion      2.3
SerializationVersion           1.1.0.1
```
## Get-Help xyz

Get-Help is the cmdlet to get help information of other cmdlet. For example, to get help information of cmdlet Get-Module, just type _Get-Help Get-Module_. 
As the description mentioned, type _Get-Help Get-Module -Online_ will navigate your to the web page of the cmdlet where you can get detailed information and examples.

With this Get-Help cmdlet, you can get very detailed and accurate information of all cmdlets i will introduce in this post.  

Actually, there is a *help* cmdlet which introduce topic "Windows PowerShell Help System".

```powershell
PS C:\Users\lxzhu> Get-Help Get-Module

NAME
    Get-Module

SYNTAX
    Get-Module [[-Name] <string[]>] [-FullyQualifiedName <ModuleSpecification[]>] [-All]  [<CommonParameters>]

    Get-Module [[-Name] <string[]>] -PSSession <PSSession> [-FullyQualifiedName <ModuleSpecification[]>] [-ListAvailable] [-PSEdition <string>] [-Refresh]  [<CommonParameters>]

    Get-Module [[-Name] <string[]>] -ListAvailable [-FullyQualifiedName <ModuleSpecification[]>] [-All] [-PSEdition <string>] [-Refresh]  [<CommonParameters>]

    Get-Module [[-Name] <string[]>] -CimSession <CimSession> [-FullyQualifiedName <ModuleSpecification[]>] [-ListAvailable] [-Refresh] [-CimResourceUri <uri>] [-CimNamespace <string>]  [<CommonParameters>]


ALIASES
    gmo


REMARKS
    Get-Help cannot find the Help files for this cmdlet on this computer. It is displaying only partial help.
        -- To download and install Help files for the module that includes this cmdlet, use Update-Help.
        -- To view the Help topic for this cmdlet online, type: "Get-Help Get-Module -Online" or
           go to https://go.microsoft.com/fwlink/?LinkID=141552.
```

## $_

*$_* is the way to represent the current object. It is used when you want to reference the output object from previous cmd let. Here are two examples

This script used *Where* to filter output from Get-Command cmdlet, and then Select-Object to show the first 10 output from Where cmdlet.
```powershell
PS C:\Users\lxzhu> Get-Command | Where {$_. Name.Contains('AzVM')} | Select-Object -first 10

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Alias           Invoke-AzVMAssessPatch                             4.4.0      Az.Compute
Alias           Invoke-AzVMPatchAssess                             4.4.0      Az.Compute
Cmdlet          Add-AzVMAdditionalUnattendContent                  4.4.0      Az.Compute
Cmdlet          Add-AzVMDataDisk                                   4.4.0      Az.Compute
Cmdlet          Add-AzVMNetworkInterface                           4.4.0      Az.Compute
Cmdlet          Add-AzVMSecret                                     4.4.0      Az.Compute
Cmdlet          Add-AzVMSshPublicKey                               4.4.0      Az.Compute
Cmdlet          ConvertTo-AzVMManagedDisk                          4.4.0      Az.Compute
Cmdlet          Disable-AzVMDiskEncryption                         4.4.0      Az.Compute
Cmdlet          Get-AzVM                                           4.4.0      Az.Compute

```

## oh -pa

*oh -pa* alias *Out-Host -Paging*. This cmdlet paginate the output of previous cmdlet. It is the equavilent of 'more' or 'less' in Linux/Unix. For example *get-command | oh -pa*
shows output of get-command in a pagination way. For more details type *get-help out-host -Online*

## Write-Host vs Write-Output

*Write-Output* write data into pipeline, which means it is the output/return value that will be passed to next cmdlet.

*Write-Host* is a wrapper of *Write-Information* which write message into host in information level. It is a part of *logging* concept. Other than *Write-Information*,
one can also *Write-Verbose*, *Write-Debug*, *Write-Warning* and *Write-Error*.

## Get-Member

*Get-Member* is a part of reflection concept. It helps you get available members (properties and methods) of an object. 
This cmdlet is very useful during your navagating the powershell.


## Module and Command cmdlets

|cmd|description|examples|
|---|---|---|
|Get-Module| search modules installed on the computer.|get-module -All|

## File System

|cmd|description|examples|
|---|---|---|
|Test-Path| test if a path exists |test-path "C:\Users\lxzhu"|

...
