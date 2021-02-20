#!/bin/bash
docker run -d \
    --name postgres-mtrade \
    -p 5432:5432 \
    -e "POSTGRES_PASSWORD=postgrespass" \
    postgres:12.6
