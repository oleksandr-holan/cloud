# Lab 1

## Registration to Heroku and Set Up of Cloud Environment

1. Go to the Sign Up page <https://signup.heroku.com/>.
2. Enter the required details and click 'Create your account'.
3. You should receive a letter to confirm your email.
4. Follow the link in the letter and create a password.
5. Add your credit card at <https://heroku.com/verify>

## Heroku Installation

1. Install scoop:

    ```sh
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    Invoke-RestMethod -Uri <https://get.scoop.sh> | Invoke-Expression
    ```

2. Install heroku-cli using scoop:

    ```sh
    scoop bucket add main
    scoop install main/heroku-cli
    ```

3. Log in:

    ```sh
    heroku login
    ```

    Confirm the log in the browser

4. Create a new Heroku app

    ```sh
    heroku create your-app-name
    ```
