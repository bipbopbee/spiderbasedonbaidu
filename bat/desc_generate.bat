@echo off
path = %path%;.\..\bin\;
desc_tools.exe 参数1 参数2 参数3
setlocal enabledelayedexpansion
for  %%x in (*.mp4, *.mkv, *.flv) do (
    set abc=%%x
    desc_tools.exe %%x 
)
pause