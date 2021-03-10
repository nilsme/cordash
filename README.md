# README

## Requirements

The dash application needs [docker_cordash](https://github.com/nilsme/docker_cordash)
as a basic infrastructure that  provides a reverse proxy (with ssl), and a
postgres database to store the application data.

This repository needs to be mounted as a `/code` for the containerized
dash-service. The default configuration expects this repository in
`~/git/cordash`. Changes can be made to the `docker-compose.yml` of
[docker_cordash](https://github.com/nilsme/docker_cordash).

## Quickstart

Deploy the infrastructure as mentioned in the requirements. Data can be loaded
by an automatic ETL process that will read the data and store it in a postgres
database provided by [docker_cordash](https://github.com/nilsme/docker_cordash).
To start the ETL process execute:

```shell script
python etl_corona_data.py
```

The dashboard will automatically update at the host's address at
`https://localhost:8080`.
