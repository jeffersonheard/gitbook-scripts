#!/bin/bash

cd website
http-server &
sleep 2s
firefox http://localhost:8080
