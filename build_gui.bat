@echo off
chcp 65001 >nul
echo ============================================================
echo AutoQuant 量化系统 编译脚本
echo ============================================================
echo.

REM 清理旧文件
echo [1/4] 清理旧编译文件...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

REM 编译策略分析平台
echo.
echo [2/4] 编译策略分析平台 (GUI)...
echo 请等待，这可能需要5-30分钟...
"C:\Users\sky1c\AppData\Roaming\Python\Python313\Scripts\pyinstaller.exe" AutoQuant-GUI.spec --clean

if exist "dist\AutoQuant-策略分析平台.exe" (
    echo.
    echo [OK] 策略分析平台编译成功!
) else (
    echo.
    echo [ERROR] 编译失败，请检查错误信息
)

echo.
echo ============================================================
echo 编译完成！
echo ============================================================
pause