#!/usr/bin/env bash

for d in "logs" "data/scraping" "data/matching" "web/data" "web/external"; do
    if [[ ! -d ${d} ]]; then
        mkdir -p ${d}
    fi
done
