#!/usr/bin/env bash
docker build -t nlmc_hosting/phpmyadmin phpmyadmin
cp -r ../frontend frontend/app
docker build -t nlmc_hosting/frontend frontend
rm -r frontend/app
