#!/usr/bin/env bash

for d in "logs" "data/jobs_scraper/indeed"; do
    if [[ ! -d "$d" ]]; then
        mkdir -p "$d"
    fi
done
