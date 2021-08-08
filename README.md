# garrascobike-be

## Environment variables

- Backblaze credentials required in order to download the ML model

- Locally setup:
    - create a `./garrascobike_be/.env` file coping the `.env_example` and rename in it `.env`
    - Fill the variables with your credentials
- Publish to the heroku service:
    - use the command `heroku config:set` to set the variables

## Heroku

- Command snippets:
    - Scale the workers (0 to disable): <br>
      `heroku ps:scale web=0`, `heroku ps:scale web=1`

    - Publish new version (tip: is a gitflow approach): <br>
      `git push heroku main`
