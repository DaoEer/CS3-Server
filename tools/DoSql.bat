@echo off
echo ===========������Ҫִ�е�sql�ļ���===========
set /p sqlFile=
echo ===========��ʼִ�� sql�ļ�:%sqlFile%===========
set curpath=%~dp0
if exist "C:\Program Files\MySQL\MySQL Server 5.7\bin\" (
	set mysqlPath="C:\Program Files\MySQL\MySQL Server 5.7\bin\"
) else (
	set mysqlPath="C:\Program Files\MySQL\MySQL Server 5.5\bin\"
)

pause
C:
cd %mysqlPath%
mysql -h localhost -uroot -p123456 <%curpath%%sqlFile%>>%curpath%sql.log 2>&1
echo ===========���sql�ļ������ִ�У��س��ر�===========
pause