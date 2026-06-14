@echo off
echo ============================================
echo AutoQuant 打包脚本
echo ============================================
echo.

echo [1/3] 安装依赖...
pip install PyQt5 matplotlib pyinstaller openai anthropic -q

echo [2/3] 清理旧文件...
if exist dist\AutoQuant.exe del dist\AutoQuant.exe
if exist build rmdir /s /q build

echo [3/3] 开始打包...
pyinstaller AutoQuant.spec --clean

echo.
echo ============================================
if exist dist\AutoQuant.exe (
    echo 打包成功！
    echo 输出文件: dist\AutoQuant.exe
    echo 文件大小:
    for %%I in (dist\AutoQuant.exe) do echo %%~zI bytes
) else (
    echo 打包失败，请检查错误信息
)
echo ============================================
pause