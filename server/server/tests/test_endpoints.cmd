@echo off
setlocal EnableDelayedExpansion

:: ================================
::  USTAWIENIA
:: ================================
:: Adres Twojego API
set SERVER=http://localhost:8000

:: Dane do rejestracji / logowania
set EMAIL=testuser@example.com
set PASSWORD=testpass123
set NEW_PASSWORD=newpass456

:: Ręcznie wklej tutaj swój access token (po wcześniejszym zalogowaniu)
set TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ4NTg4MjYyLCJpYXQiOjE3NDg1ODc5NjIsImp0aSI6ImEzMWNkZTZmN2M2ZTQ2MjY5NzgyMTA4Zjc5MWRmYmM3IiwidXNlcl9pZCI6Mn0.2s2dIfIrrfG-kVAjLYTyDn7kHFQ1snjxbVsQL87BcWA

:: ================================
:: 1) Sign Up
:: ================================
echo.
echo ==== 1. Sign Up ====
curl -X POST %SERVER%/api/signup/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"email\":\"%EMAIL%\",\"password\":\"%PASSWORD%\"}"
echo.
echo.

:: ================================
:: 2) Login (niezbędne, aby pobrać token)
::    Uwaga: tutaj tylko demonstracja – token ustawiasz ręcznie
:: ================================
echo ==== 2. Login (tylko demo) ====
curl -X POST %SERVER%/api/token/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%EMAIL%\",\"password\":\"%PASSWORD%\"}"
echo.
echo.

:: ================================
:: 3) Get current user (GET /api/get_user/)
:: ================================
echo ==== 3. Get current user ====
curl -X GET %SERVER%/api/get_user/ ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 4) Reset Password
:: ================================
echo ==== 4. Reset Password ====
curl -X POST %SERVER%/api/reset_password/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"%EMAIL%\",\"new_password\":\"%NEW_PASSWORD%\"}"
echo.
echo.

:: ================================
:: 5) Follow User
::    Podmień "otheruser" na istniejącego użytkownika
:: ================================
echo ==== 5. Follow User ====
curl -X POST %SERVER%/api/follow_user/ ^
  -H "Authorization: Bearer %TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"otheruser\"}"
echo.
echo.

:: ================================
:: 6) Unfollow User
:: ================================
echo ==== 6. Unfollow User ====
curl -X POST %SERVER%/api/unfollow_user/ ^
  -H "Authorization: Bearer %TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"otheruser\"}"
echo.
echo.

:: ================================
:: 7) Create Challenge
:: ================================
echo ==== 7. Create Challenge ====
curl -X POST %SERVER%/api/create_challenge/ ^
  -H "Authorization: Bearer %TOKEN%" ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"30 Days Coding\",\"type\":\"daily\",\"description\":\"Codzienne programowanie\",\"frequency\":1,\"duration\":30}"
echo.
echo.

:: ================================
:: 8) List Challenges
:: ================================
echo ==== 8. List Challenges ====
curl -X GET %SERVER%/api/list_challenges/ ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 9) Get Followers
:: ================================
echo ==== 9. Get Followers ====
curl -X GET %SERVER%/api/get_followers/testuser/  ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 10) Get Following
:: ================================
echo ==== 10. Get Following ====
curl -X GET %SERVER%/api/get_following/testuser/  ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 11) List User Posts
:: ================================
echo ==== 11. List User Posts ====
curl -X GET %SERVER%/api/list_user_posts/testuser/  ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 12) Get User Badges
::    Podmień USER_ID na ID testowego usera
:: ================================
set USER_ID=1
echo ==== 12. Get User Badges (user %USER_ID%) ====
curl -X GET %SERVER%/api/users/%USER_ID%/badges/ ^
  -H "Authorization: Bearer %TOKEN%"
echo.
echo.

:: ================================
:: 13) Get User Profile Data
:: ================================
echo ==== 13. Get User Profile Data ====
curl -X GET %SERVER%/api/userprofile/testuser/
echo.
echo.

pause
