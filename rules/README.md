## PLIS 规则库整体结构
🟦 协议 / 横向 / 信息收集（Network & Lateral Movement）

| 文件名 | 中文名称 |
|--------|----------|
🔹 Active Directory（AD）
| ad-priv.yml | Active Directory 提权规则 |
| ad.yml | Active Directory 通用规则 |
| esc.yml | 权限逃逸 / 提权规则（Escalation） |
🔹 SMB / 网络扫描
| nmap.yml | Nmap 扫描解析规则 |
| smb.yml | SMB 协议漏洞规则 |

🟦 Web 漏洞集（Web Vulnerabilities）

待补充
🟦 network
```
 network/
    smb.yml
    ldap.yml
    rdp.yml
    ftp.yml
    ssh.yml
    smtp.yml
    snmp.yml
    dns.yml
    mysql.yml
    mssql.yml
    redis.yml
    nfs.yml
    winrm.yml
```
🟦 system
```
system/
    privilege_escalation.yml
    windows_privesc.yml
    linux_privesc.yml
    sudo.yml
    capabilities.yml
    suid.yml
    kernel.yml
    cronjob.yml
    weak_file_perm.yml
    backup_files.yml
    docker_breakout.yml
```
🟦 ad
```
 ad/
    kerberoasting.yml
    asreproast.yml
    zerologon.yml
    pass_the_hash.yml
    pass_the_ticket.yml
    unconstrained_delegation.yml
    constrained_delegation.yml
    dns_admin.yml
    ldap_signing.yml
    nopac.yml
```
🟦 misconfig
```
misconfig/
    default_creds.yml
    weak_password.yml
    exposed_panels.yml
    directory_listing.yml
    debug_mode.yml
    backup_files.yml
```
🟦 iot
```
iot/
    rtsp.yml
    upnp.yml
    modbus.yml
    bacnet.yml
```
🟦 cloud
```
cloud/
    s3.yml
    iam.yml
```


