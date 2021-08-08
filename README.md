# garrascobike-be

## Environment variables

- Backblaze credentials are required in order to download the ML model

- Setup environment variables:
    - Locally: create a `./garrascobike_be/.env` file (you can copy the `.env_example` and rename in it `.env`)
    - Heroku: use the command `heroku config:set` to set the variables
- ℹ Those are the variables required:
    - BB_APP_KEY_NAME=garrascobike-downloader
    - BB_APP_KEY=K0xxxxxxxxxxxxxxxxx
    - BB_APP_KEY_ID=00xxxxxxxxxxxxxxxxx

## Heroku

- Command snippets:
    - Scale the workers to 0 (disabled) or to _N_: `heroku ps:scale web=0`, `heroku ps:scale web=1`
