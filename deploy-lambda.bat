@echo off
echo 🚀 Deploying Chatbot to AWS Lambda (FREE)
echo ========================================

echo 📋 Prerequisites:
echo 1. AWS CLI configured (aws configure)
echo 2. SAM CLI installed
echo 3. Your Groq API key ready
echo.

pause

echo 🔨 Building SAM application...
sam build

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo 🚀 Deploying to AWS...
sam deploy --guided

echo ✅ Deployment complete!
echo Your API will be available at the URL shown above
pause