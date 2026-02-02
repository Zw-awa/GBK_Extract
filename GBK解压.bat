@echo off
chcp 65001 >nul
title GBK编码解压工具

:: 设置路径
set "PYTHON_SCRIPT=%~dp0GBK_Extract.py"
set "PYTHON_EXE=python"

echo 正在使用GBK编码解压: %1
echo.

:: 检查是否拖放了文件
if "%~1"=="" (
    echo 错误：请将压缩文件拖放到此批处理文件上
    echo.
    echo 或者直接运行: %0 "压缩文件.zip"
    pause
    exit /b
)

:: 检查文件是否存在
if not exist "%~1" (
    echo 错误：文件不存在 - %~1
    pause
    exit /b
)

:: 运行Python脚本
"%PYTHON_EXE%" "%PYTHON_SCRIPT%" "%~1"

if errorlevel 1 (
    echo 解压失败！
) else (
    echo 解压完成！
)

pause