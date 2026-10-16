@echo off
chcp 65001 >nul
title RMtech - Đẩy Mã Nguồn Lên GitHub (A* Search)

echo ========================================================
echo   RMtech - Đẩy Code Lên GitHub: snake-game-astar
echo   Tổ chức: https://github.com/RMtech-Studio
echo ========================================================
echo.

cd /d "%~dp0"
set "PATH=C:\Users\son\AppData\Local\Programs\Git\cmd;C:\Windows\System32\OpenSSH;%PATH%"

git init -b main
git config user.name "RMtech-Studio"
git config user.email "contact@rmtech.studio"
git add .
git commit -m "feat: Initial commit for Episode 02 - Snake Game AI with A* Search"
git remote add origin git@github.com:RMtech-Studio/snake-game-astar.git 2>nul
git remote set-url origin git@github.com:RMtech-Studio/snake-game-astar.git

echo [*] Đang đẩy code lên GitHub...
git push -u origin main

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo   [V] ĐẨY CODE LÊN GITHUB THÀNH CÔNG RỰC RỠ!
    echo   Kho lưu trữ: https://github.com/RMtech-Studio/snake-game-astar
    echo ========================================================
) else (
    echo.
    echo [!] Nếu kho chưa được tạo trên GitHub, vui lòng tạo repo trống:
    echo     https://github.com/new -> Tên: snake-game-astar (Public)
    echo     Sau đó chạy lại file .bat này!
)

echo.
pause
