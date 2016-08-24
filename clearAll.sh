#!/usr/bin/env bash

# Checks if the results directory exists and cleans the environment
if [  -d "results" ]; then

  echo "[MAIN] Cleaning environment..."
  rm -r results

fi