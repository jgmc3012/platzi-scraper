# MyPyppertter

## Install project
```sh
pip install -r requirements.txt
./init.local.sh build
```

## Run Scraper
### Open Browser

If you are using WSL see the next [post](https://virtualizationreview.com/articles/2017/02/08/graphical-programs-on-windows-subsystem-on-linux.aspx) and [this](https://code.luasoftware.com/tutorials/x-server/xming-client-4-rejected-from-ip/) if you hace any problem with the permissions with Xming
```sh
# Use python 3.8(equal dockerfile)
source .envs/.local/.postgres
export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python console.py  pyppeteer:open_browser
```