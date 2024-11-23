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
Копировать код
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

```bash
https://www.kaggle.com/datasets/jrobischon/wikipedia-movie-plots
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

1 . Clone repo
[Connect with SSH](https://bostongene.atlassian.net/wiki/spaces/HDM/pages/1237057537/Bitbucket)

```bash
git clone git@bitbucket.org:bostongene/hippocrates-backoffice-backend.git
```

2 . Install requirements

For backend:

1. Download Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 - --version 1.8.1
```


2. Export its path.

   Note: there is going to be a command recommanded for you to export to path.
```bash
export PATH="$HOME/.local/bin:$PATH"
```

 You can check if poetry was installed correctly with this command:
```bash
poetry --version
```

3. Enter the virtual env and download the dependencies with these commands:
```bash
virtualenv venv -p python3.11
source venv/bin/activate
poetry install --with development
```

## Working with Poetry

All the dependencies and poetry configs are in pyproject.toml and poetry.toml.
In the pyproject.toml you have all the dependencies separated into groups;
```[tool.poetry.dependencies]``` - for main dependencies,
```[tool.poetry.group.development.dependencies]``` - for development dependencies,
```[tool.poetry.group.code-style.dependencies]``` - for code-style checking dependencies,
and so on.

To add new dependencies or change versions all you need to do is to
go to pyproject.toml and add the dependency
to the corresponding group.

If during the download you encounter problems we suggest:

Method 1. Delete and remake the virtual env:

  ```bash
  virtualenv venv -p python3.11
  source venv/bin/activate
  ```

Method 2. Downloading poetry with pip.

1. Deleting the existing
   poetry and reinstall it using pip
  ```bash
  curl -sSL https://install.python-poetry.org | python3 - --uninstall
  curl -sSL https://install.python-poetry.org | POETRY_UNINSTALL=1 python3 -
  pip install poetry==1.8.1
  ```
2. Delete the venv folder and then reactivate it like in the steps above:
  ```bash
  virtualenv venv -p python3.11
  source venv/bin/activate
  ```
3. Try to install with poetry again
  ```bash
  poetry install --with development
  ```

If you still encounter problems with downloading, then try
downloading the failed dependencies with pip.

```bash
pip install <name of dependency>==<version>
```

If even that is not helping, you can use this command for poetry to
convert the dependencies into a requirements.txt file and download it in that manner.

```bash
poetry export --without-hashes --format=requirements.txt > requirements.txt
pip install -r requirements.txt
```

## How to debug tests in VS Code

Предусловия:

1. Установить свежую версию [VS Code](https://code.visualstudio.com/Download)
1. Установить расширение [ms-vscode-remote.vscode-remote-extensionpack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack)

Ограничения:

1. Пока можно отлаживать и запускать только API Backend

После запуска `VS Code` выполнить команду `> Remote-Containers: Reopen in Container` и дождаться, когда завершиться сборка и
инициализации окружения. Какое-то время VS Code может потратить на конфигурацию Python-окружения в IDE:

![Remote container initialization](./doc/remote-container-1.png)

После запускаем команда `> Python: Run All Tests`:

![Run all tests](./doc/remote-container-2.png)

Подробная информация о том, как работать с VS Code и Docker Container, читайте [Remote containers](https://code.visualstudio.com/docs/remote/containers).

### How to fill/update database

Изменение системных настроек для [корректной работы ElasticSearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html)

    sudo sysctl -w vm.max_map_count=262144

1 . Install requirements:

```bash
poetry install --with development
```

2  . Install pre-commit hook

```bash
# For commit without pre-commit hook add --no-verify to your commit command)
# Example: git commit --no-verify -m 'test'
pre-commit autoupdate
pre-commit install
```

3 . Run database (will still run when the system is restarted)

```bash
sudo docker-compose -f ./.devcontainer/docker-compose.services.yml up -d elasticsearch postgres flower redis
```

4 . Run migrations

```bash
alembic upgrade head
```

5 . To populate the database, run backend and locally run deploy in hippocrates-ldt with source selectors.
Watch [README.md](https://bitbucket.org/bostongene/hippocrates-ldt/src/master/README.md) hippocrates-ldt for more information. See [list of dumps](https://docs.google.com/spreadsheets/d/188oZ2h1sFw4D9wLqOWwZrW9LyKYdy7gurdi9aWpeZPE/edit?pli=1#gid=1253238620) which are necessary for Backoffice web app deployment.

6 . For deploy clinical-trials, you need the latest version of the treatments


### Миграции в Базе данных

Если пришлось внести изменения в структуру таблиц PostgreSQL необходимо применить следующую команду:

```
alembic revision --autogenerate -m "Комментарий"
```

В случае, если были несовместимые изменения, миграции необходимо применять вручную.

### Creating OpenSearch indices

Use the command to create indices in OpenSearch:

```bash
curl -X PUT "localhost:9200/<index_name>?pretty"
```

where `index_name`:

1. `matched_documents`
2. `drugs`
3. `cohort_page`
4. `trials_page`
5. `user_events`
6. `locations_cities`
7. `locations_states`
8. `locations_countries`

### Дамп базы данных
Локальный запуск скрипта с обновлением базы данных может выполняться достаточно долго.
В случае если нет необходимости отслеживать процесс обновления вручную, БД можно взять snapshot с сервера.
Для этого запустите скрипт ./scripts/db-dump.sh со следующими опциями:
```
--host=<remote host>  # required
--port=<remote port>  # optional, по умолчанию 5432
--db=<remote db>  # required
--user=<remote user>  # required
--password=<remote password>  # required
--table=<table name> # required
--rm  # optional, флаг, используется для удаления файла с дампом после наполнения локальной БД
```

### Run backend:

1. Find out your auth API-key in API-KEYS page: https://api.dev.bostongene.internal

2. Run this commands with your **APIKEY**:

```bash
export BG_KEY=<YOUR APIKEY>
export AWS_ACCESS_KEY_ID=<YOUR S3 ACCESS ID>
export AWS_SECRET_ACCESS_KEY=<YOUR S3 ACCESS KEY>
export BG_RND_KEY=<ANOTHER APIKEY>
```

```bash
cd src
python web_app_local_run.py
```

In another terminal (with also all export keys before):
```bash
celery -A src.consumer_run.app worker
```
## Локальный запуск через докер

0 . [Optional] Если базы не подняты, запустить Postgre и Elastic из папки *.devcontainer/* командой ```docker compose -f ./docker-compose.services.yml up```. Для использования сети хоста добавить 'network_mode: host'.

1 . Из корня проекта запустить ```docker build -t backend:local .```

2 . Поменять секреты *.env.example* на валидные ключи

3 . Запустить веб-приложение командой ```docker run -d --network host --name localback --env-file ./.env.example -p 5000:5000 backend:local python src/web_app_local_run.py```

4 . [Optional] Если postgre пустая, запустить миграции командой ```docker exec localback alembic upgrade head```

5 . Запустить воркеры командой ```docker exec localback celery -A src.consumer_run.app worker```

6 . Бэкенд будет запущен на 5000 порту, проверить его работоспособность можно на [http://localhost:5000/ui/#/](этой странице)

## Code quality and tests

### Backend

Run tests

```bash
python -m pytest src/tests/unit_tests
python -m pytest src/tests/integration_tests
pytest e2e --app-url=<host:port> --api-key=<your apikey>  # by default --app-url=http://localhost:5000 --api-key=""
```

Unit tests with coverage calculation and HTML report:

```bash
coverage run --source=./src -m pytest -k unit_tests && coverage html
```

Integration tests with coverage calculation and HTML report:

```bash
coverage run --source=./src -m pytest -k integration_tests && coverage html
```

Unit and integration tests with coverage calculation and HTML report
```bash
coverage run --source=./src -m pytest -k "unit_tests or integration_tests" && coverage html
```

*(HTML report could be found at `htmlcov` folder)*

Run code formatter

```bash
ruff format apps
```

Run code linter

```bash
ruff check apps --fix
```

Run type checking

```bash
## For newly added files in the current branch
git diff development --name-only --diff-filter=A | grep .py | pyright -
## For modified and added files in the current branch
git diff development --name-only --diff-filter=AM | grep .py | pyright -
```

## Continuous delivery

### Pipelines

1. Build - https://concourse.bostongene.internal/?search=team%3A%22hippocrates%22%20group%3A%backoffice-backend-build%22
2. State - https://concourse.bostongene.internal/teams/hippocrates/pipelines/backoffice-backend-state
3. PR - https://concourse.bostongene.internal/?search=team%3A%22hippocrates%22%20group%3A%backoffice-backend-pr%22
4. Utils - https://concourse.bostongene.internal/teams/hippocrates/pipelines/backoffice-backend-utils

# Release management process
SOP - https://bostongene.atlassian.net/wiki/spaces/KBS/pages/4171366672/RAX+AWS

### Обновление pipeline'a

    fly --target bg login --team-name hippocrates --concourse-url https://concourse.bostongene.internal

    fly -t bg set-pipeline -p backoffice-backend-utils -c .concourse/pipelines/utils.yml -l .concourse/vars.yml
    fly -t bg set-pipeline -p backoffice-backend-state -c .concourse/pipelines/state.yml -l .concourse/vars.yml
    fly -t bg set-pipeline -p backoffice-backend-pr -c .concourse/pipelines/pr.yml -l .concourse/vars.yml -i number=PR_NUMBER_HERE
    fly -t bg set-pipeline -p backoffice-backend-build -c .concourse/pipelines/build.yml -l .concourse/vars.yml

### Commands

To unpause job:

    fly -t bg unpause-job --job backoffice-backend-<pipeline>/<job-name>

To validate pipeline:

    fly -t bg validate-pipeline -c .concourse/pipelines/utils.yml  --enable-across-step
    fly -t bg validate-pipeline -c .concourse/pipelines/state.yml  --enable-across-step
    fly -t bg validate-pipeline -c .concourse/pipelines/pr.yml  --enable-across-step
    fly -t bg validate-pipeline -c .concourse/pipelines/build.yml  --enable-across-step

Check PR:

For manual invoking build-pr job for specific PR you can leave a comment **/test this** on the bitbucket PR's page

## K8S deployment

* Сервис разворачивается k8s с помощью двух job в Concourse-pipeline: stage-deploy и prod-deploy
* Доступные **namespace** - _dev-hippocrates_, _rnd-hippocrates_
* stage-deploy разворачивает сервис в namespace - dev-hippocrates
* prod-deploy разворачивает сервис в namespace - rnd-hippocrates
* Для проведения операций с сервисом в k8s можно использовать **kubectl** (CLI приложение).
* [Инструкция по установке и настройке Kubernetes](https://bostongene.atlassian.net/wiki/spaces/PLT/pages/3624042517/K8s+-+User+guide)
* [Инструкция по настройке авторизации для доступа к кластеру](https://bostongene.atlassian.net/wiki/spaces/ITOPS/pages/3512336433/K8s+new#%D0%9D%D0%B0%D1%81%D1%82%D1%80%D0%BE%D0%B9%D0%BA%D0%B0-kubernetes)
* [Troubleshooting guide](https://bostongene.atlassian.net/wiki/spaces/PLT/pages/1240432641/Kubernetes+deployments+troubleshooting+guide)
* Команда для просмотра последних логов сервиса.
      `kubectl logs -f -n <namespace> -l app=backoffice-backend`
* Команда для просмотра активных подов.
      `kubectl get pods -n <namespace>`
* Посмотреть логи конкретного пода. **podId** берем из вывода в предыдущем пункте
      `kubectl logs -n <namespace> <podId>`

## Monitoring

Для мониторинга можно воспользоваться сервисом Grafana.

Dashboard Hipp/Backoffice находится по адресу:
  https://grafana.rax.bostongene.internal/d/bPES3c2nk/hippocrates-backoffice

## Other operations

Обновить список клинических центров:

    pip install googlemaps==4.6.0
    export BG_KEY=<YOUR RND APIKEY>
    export REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
    python src/utils/process_clinical_centers.py
