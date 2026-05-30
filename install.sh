#!/bin/bash
# install.sh - نصب خودکار API Security Auditor Pro

set -e

echo "🔒 Installing API Security Auditor Pro..."

# بررسی نسخه پایتون
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [[ $(echo "$python_version" | cut -d. -f1,2) < "$required_version" ]]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# ایجاد محیط مجازی
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# آپگرید pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# نصب وابستگی‌ها
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# نصب در حالت توسعه
echo "🔧 Installing package in development mode..."
pip install -e .

# نصب pre-commit hooks (اختیاری)
if [ -f ".pre-commit-config.yaml" ]; then
    echo "🐍 Installing pre-commit hooks..."
    pre-commit install
fi

echo "✅ Installation complete!"
echo ""
echo "🚀 To activate the environment:"
echo "   source venv/bin/activate"
echo ""
echo "🎯 To run the tool:"
echo "   api-auditor --help"