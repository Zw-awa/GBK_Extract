@echo off
chcp 65001 >nul
title 移除右键菜单

echo 正在移除右键菜单...

reg delete "HKCR\*\shell\用GBK编码解压\command" /f
reg delete "HKCR\*\shell\用GBK编码解压" /f

echo 右键菜单已移除
pause