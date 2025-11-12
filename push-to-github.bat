@echo off
setlocal enabledelayedexpansion

echo ================================
echo Git Push Automation Script
echo ================================

cd /d "C:\Users\LENOVO\OneDrive\Documents\AI Panduan Penggunaan Aplikasi JKN\AI-Panduan-JKN"

echo.
echo [STEP 1] Setting git user config...
"C:\Program Files\Git\cmd\git.exe" config --global user.email "ranwrn07@gmail.com"
"C:\Program Files\Git\cmd\git.exe" config --global user.name "Ran Warna"
echo [OK] Git config set

echo.
echo [STEP 2] Current directory:
cd

echo.
echo [STEP 3] Initializing git repository...
"C:\Program Files\Git\cmd\git.exe" init
echo [OK] Git initialized

echo.
echo [STEP 4] Adding all files...
"C:\Program Files\Git\cmd\git.exe" add .
echo [OK] Files added

echo.
echo [STEP 5] Creating commit...
"C:\Program Files\Git\cmd\git.exe" commit -m "Initial commit: semua file siap deploy"
echo [OK] Commit created

echo.
echo [STEP 6] Setting remote origin...
"C:\Program Files\Git\cmd\git.exe" remote remove origin 2>nul
"C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/ranwrn07-png/-AI-Panduan-JKN.git
echo [OK] Remote origin set

echo.
echo [STEP 7] Renaming branch to main...
"C:\Program Files\Git\cmd\git.exe" branch -M main
echo [OK] Branch renamed

echo.
echo [STEP 8] Pushing to GitHub...
"C:\Program Files\Git\cmd\git.exe" push -u origin main
echo [OK] Push completed

echo.
echo ================================
echo [OK] SEMUA SELESAI! Repo sudah di push ke GitHub.
echo Cek: https://github.com/ranwrn07-png/-AI-Panduan-JKN
echo ================================

pause
