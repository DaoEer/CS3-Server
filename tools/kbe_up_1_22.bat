@echo off
set sqlFile="kbe_up_1_22.sql"
echo ===========��ʼִ�� sql�ļ�:%sqlFile%===========
set curpath=%~dp0
set mysqlPath="C:\Program Files\MySQL\MySQL Server 5.7\bin\"
C:
cd %mysqlPath%
mysql -h localhost -uroot -p123456 <%curpath%%sqlFile%>>%curpath%sql.log 2>&1
echo ===========���sql�ļ������ִ�У��س��ر�===========
pause