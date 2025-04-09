@ECHO Off
ipconfig | find /i "IPv4" > t.txt
for /f "tokens=14* delims=: " %%i in (t.txt) do ( 
set "IP=%%j" 
goto next1:
)
:next1
del t.txt
ECHO %IP%

set "ymd=%date:~,4%-%date:~5,2%-%date:~8,2%"
if exist logs (
cd logs
if not exist tftp (md tftp)
for %%f in (*.*) do (type %%f|find "%ymd%">E:\svn\CS3-Server\logs\tftp\%%f)
cd tftp
for %%f in (*.*) do (tftp 172.16.6.205 put %%f %IP%.%%f)

cd ..\..
)
