@echo off
echo ========================================
echo SHAIKHTONAK Data Analysis Runner
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if data directory exists
if not exist "data" (
    echo Error: Data directory not found
    echo Please ensure the data directory is in the correct location
    pause
    exit /b 1
)

echo Starting comprehensive data analysis...
echo.

REM Run the comprehensive analysis
python run_comprehensive_data_analysis.py --data-root data --verbose

echo.
echo Analysis complete!
echo.
echo Results saved to:
echo   - comprehensive_analysis_results.json
echo   - comprehensive_analysis_summary.md
echo   - comprehensive_analysis.log
echo.

pause
