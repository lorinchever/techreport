#!/usr/bin/env bash

for d in "logs" "data/jobs_scraper/indeed" "data/jobs_matching/indeed"; do
    if [[ ! -d "$d" ]]; then
        mkdir -p "$d"
    fi
done
