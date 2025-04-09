@echo off

for /f "tokens=4" %%a in ('route print^|findstr 0.0.0.0.*0.0.0.0') do (
 set ip=%%a
	goto out
)
:out

echo ip = %ip%
for /f "tokens=1-4 delims=." %%a in ("%ip%") do set strip=%%~a%%~b%%~c%%~d
echo strip = %strip%
set uid=%strip%

C:\Python34\python .\kbe\tools\server\pycluster\cluster_controller.py shutdown