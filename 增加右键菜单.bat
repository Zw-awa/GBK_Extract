@echo off
chcp 65001 >nul
title 添加GBK解压到右键菜单

:: 获取当前目录
set "CURRENT_DIR=%~dp0"
set "BAT_PATH=%CURRENT_DIR%GBK解压.bat"

echo 正在添加右键菜单...
echo 批处理文件路径: %BAT_PATH%
echo.

:: 为ZIP文件添加右键菜单
reg add "HKCR\*\shell\用GBK编码解压" /ve /t REG_SZ /d "用GBK编码解压" /f
reg add "HKCR\*\shell\用GBK编码解压\command" /ve /t REG_SZ /d "\"%BAT_PATH%\" \"%%1\"" /f

echo 右键菜单添加成功！
echo 现在可以在任何文件上右键选择"用GBK编码解压"
echo.
pause