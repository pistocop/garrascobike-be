# garrascobike-be

## Environment variables

- Backblaze credentials required in order to download the ML model

- Setup environment variables:
    - Locally: create a `./garrascobike_be/.env` file coping the `.env_example` and rename in it `.env`
    - Fill the variables with your credentials
- Publish to the heroku service:
    - use the command `heroku config:set` to set the variables

## Heroku

- Command snippets:
    - Scale the workers to 0 (disabled) or to _N_: `heroku ps:scale web=0`, `heroku ps:scale web=1`
