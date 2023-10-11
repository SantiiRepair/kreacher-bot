#!/bin/bash

export $(cat .env | xargs)
make start