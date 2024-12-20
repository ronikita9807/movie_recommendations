# README

## About

A project that provides tools for recommend movies by summary and by personal choice

The project uses Python 3.12

## Установка зависимостей
```bash
pip install requirements.txt
```
```bash
python -m spacy download en_core_web_sm
```
## Проблема с установкой psycopg2:


```bash
brew install openssl@1.1
```

```bash
brew --prefix openssl@1.1
```

```bash
export LDFLAGS="-L$(brew --prefix openssl@1.1)/lib"
export CPPFLAGS="-I$(brew --prefix openssl@1.1)/include"
export PATH="/opt/homebrew/opt/openssl@1.1/bin:$PATH"
```

```bash
source ~/.zshrc
source ~/.bash_profile
```

```bash
env LDFLAGS="-L$(brew --prefix openssl@1.1)/lib" CPPFLAGS="-I$(brew --prefix openssl@1.1)/include" pip install psycopg2
```

```bash
pip install psycopg2-binary
```


## Data source:
### Save csv file
```bash
by path: apps/shared/core/service/data/movies_dataset.csv
https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots
```
### Save vectors data
```bash
by path: apps/shared/core/service/data/googlenews-vectors-negative300.bin
https://www.kaggle.com/datasets/leadbest/googlenewsvectorsnegative300
```

## Run code formatter

```bash
ruff format apps
```

## Run code linter

```bash
ruff check apps --fix
```


## How to build

```bash
uvicorn main:app --reload
```