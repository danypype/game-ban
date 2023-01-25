#!/bin/bash
. ./.env && python initdb.py
. ./.env.test && python initdb.py
