# garrascobike-be

> run on deta setup

## Setup

- Install deta [cli](https://docs.deta.sh/docs/cli/commands/)
- Log in into deta CLI
- cd into `garrascobike_be`
    - *deploy* the service
        - `deta new --name garrascobike-be --project garrascobike`
    - **update** the back-end
        - `deta deploy`
- visit [https://web.deta.sh/home/](https://web.deta.sh/home/)

## Logs
- You can see the logs visiting the webpage under the Visor tab

## Requirements
- Deta deploy looks like create a "diff" between the requirements.txt and the packages installed on the Micro.
    Then apply (install/uninstall) only the differences.
- Starlette error:
    - Even if reported under requirements.txt, the deta service fall in error during the starlette import
    - Solution: no clean solution found, but the error looks like disappear aftera a delete/recreate of the micros
