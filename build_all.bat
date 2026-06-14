@echo off
echo ============================================
echo AutoQuant 批量打包脚本
echo ============================================
echo.

setlocal enabledelayedexpansion

:: 检查是否安装了 pyinstaller
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/4] 安装 pyinstaller...
    pip install pyinstaller -q
)

:: 编译 GUI 版本
echo.
echo [2/4] 编译 AutoQuant-GUI.exe...
if exist dist\AutoQuant-GUI.exe del dist\AutoQuant-GUI.exe
if exist build rmdir /s /q build
pyinstaller AutoQuant-GUI.spec --clean
if exist dist\AutoQuant-GUI.exe (
    echo   ✓ GUI 编译成功
) else (
    echo   ✗ GUI 编译失败
)

:: 编译 vn.py 版本
echo.
echo [3/4] 编译 AutoQuant-VNPY.exe...
if exist dist\AutoQuant-VNPY.exe del dist\AutoQuant-VNPY.exe
if exist build rmdir /s /q build
pyinstaller AutoQuant-VNPY.spec --clean
if exist dist\AutoQuant-VNPY.exe (
    echo   ✓ VNPY 编译成功
) else (
    echo   ✗ VNPY 编译失败
)

:: 编译 Qlib 版本
echo.
echo [4/4] 编译 AutoQuant-QLIB.exe...
if exist dist\AutoQuant-QLIB.exe del dist\AutoQuant-QLIB.exe
if exist build rmdir /s /q build
pyinstaller AutoQuant-QLIB.spec --clean
if exist dist\AutoQuant-QLIB.exe (
    echo   ✓ QLIB 编译成功
) else (
    echo   ✗ QLIB 编译失败
)

echo.
echo ============================================
echo 编译完成！
echo 输出目录: dist\
echo --------------------------------------------
dir dist\*.exe /b
echo ============================================
pause