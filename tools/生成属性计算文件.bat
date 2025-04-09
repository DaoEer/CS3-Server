@echo off
cd ..
set pard=%cd%
cd %pard%\res\scripts\common\
python GenerateCalcProperties.py
@echo "Spanned file: %pard%\res\scripts\common\CalcProperties.py"
pause
exit