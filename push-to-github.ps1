# Script untuk push repo ke GitHub secara otomatis
# Jalankan: .\push-to-github.ps1

Write-Host "================================" -ForegroundColor Green
Write-Host "Git Push Automation Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Step 1: Set git config
Write-Host "`n[STEP 1] Setting git user config..." -ForegroundColor Yellow
git config --global user.email "ranwrn07@gmail.com"
git config --global user.name "Ran Warna"
Write-Host "✓ Git config set" -ForegroundColor Green

# Step 2: Check current directory
Write-Host "`n[STEP 2] Current directory:" -ForegroundColor Yellow
Write-Host (Get-Location)

# Step 3: Initialize git (if not already)
Write-Host "`n[STEP 3] Initializing git repository..." -ForegroundColor Yellow
git init
Write-Host "✓ Git initialized" -ForegroundColor Green

# Step 4: Add all files
Write-Host "`n[STEP 4] Adding all files..." -ForegroundColor Yellow
git add .
Write-Host "✓ Files added" -ForegroundColor Green

# Step 5: Commit
Write-Host "`n[STEP 5] Creating commit..." -ForegroundColor Yellow
git commit -m "Initial commit: semua file siap deploy"
Write-Host "✓ Commit created" -ForegroundColor Green

# Step 6: Set remote origin
Write-Host "`n[STEP 6] Setting remote origin..." -ForegroundColor Yellow
git remote remove origin 2>$null  # Remove if exists
git remote add origin https://github.com/ranwrn07-png/-AI-Panduan-JKN.git
Write-Host "✓ Remote origin set" -ForegroundColor Green

# Step 7: Rename branch to main
Write-Host "`n[STEP 7] Renaming branch to main..." -ForegroundColor Yellow
git branch -M main
Write-Host "✓ Branch renamed" -ForegroundColor Green

# Step 8: Push to GitHub
Write-Host "`n[STEP 8] Pushing to GitHub..." -ForegroundColor Yellow
git push -u origin main
Write-Host "✓ Push completed" -ForegroundColor Green

Write-Host "`n================================" -ForegroundColor Green
Write-Host "✓ SEMUA SELESAI! Repo sudah di push ke GitHub." -ForegroundColor Green
Write-Host "Cek: https://github.com/ranwrn07-png/-AI-Panduan-JKN" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Green
