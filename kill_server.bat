taskkill /f /t /im machine.exe > nul 2> nul 
taskkill /f /t /im logger.exe > nul 2> nul 
taskkill /f /t /im dbmgr.exe > nul 2> nul 
taskkill /f /t /im baseappmgr.exe > nul 2> nul 
taskkill /f /t /im cellappmgr.exe > nul 2> nul 
taskkill /f /t /im baseapp.exe > nul 2> nul 
taskkill /f /t /im cellapp.exe > nul 2> nul 
taskkill /f /t /im loginapp.exe > nul 2> nul 
taskkill /f /t /im interfaces.exe > nul 2> nul 
@rem taskkill /f /t /im bots.exe > nul 2> nul 

call "tpLogs.bat"