@echo off
echo ===========请输入要执行的sql文件名===========
set /p sqlFile=
echo ===========开始执行 sql文件:%sqlFile%===========
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
echo ===========完成sql文件的语句执行，回车关闭===========
pause