#!/bin/bash
# Creates a basic django module with minimal files in the provided path
INST_PATH="${1}"
MODULE_NAME="${2}"

if [ -z "${INST_PATH}" ]
then
    echo "Please provide an installation path"
    exit 1
fi

if [ -z "${MODULE_NAME}" ]
then
    echo "Please provide a module name"
    exit 1
fi

FULL_PATH="${INST_PATH}""${MODULE_NAME}""/"
mkdir "${FULL_PATH}"
touch "${FULL_PATH}"{__init__,models,services,tests}.py

MIGRATIONS_PATH="${FULL_PATH}"migrations/

mkdir "${MIGRATIONS_PATH}"
touch "${MIGRATIONS_PATH}"__init__.py
