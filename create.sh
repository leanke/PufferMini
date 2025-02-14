#!/bin/bash
PROJECT_NAME=$1
mkdir -p $PROJECT_NAME/
cp template/template.h $PROJECT_NAME/$1.h
cp template/template.c $PROJECT_NAME/$1.c
cp template/template.py $PROJECT_NAME/$1.py
cp template/template.pyx $PROJECT_NAME/cy_$1.pyx
cp config/template.ini config/$PROJECT_NAME.ini
echo "Project $PROJECT_NAME created"
echo "Don't forget:"
echo "    to update the config/$PROJECT_NAME.ini package and env_name"
echo "    to add to the build inplace and environtment"
