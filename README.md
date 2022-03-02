# MyPyppertter

## Install project
```sh
pip install -r requirements.txt
./init.local.sh build
```

## Run Scraper
### Open Browser
```sh
# Use python 3.8(equal dockerfile)
source .envs/.local/.postgres
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python console.py  pyppeteer:open_browser
```