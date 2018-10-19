#!/bin/bash

export FLASK_APP=server

update_db(){
    echo "migrate database"
    flask db migrate
    echo "upgrade db"
    flask db upgrade
}


init_db(){
    echo "init database"
    flask db init

    update_db

    echo "deploy default users"
    flask deploy
}


if [ "$1" = "init_db" ]
then
    init_db
elif [ "$1" = "reset_db" ]
then
    echo "remove existing_db"
    rm -rf migrations
    rm data.sqlite

    init_db
elif [ "$1" = "update_db" ]
then
    echo "Update db"
    update_db

elif [ "$1" = "init_dirs" ]
then
    echo "Create default directories"
    mkdir -p io
    cd io/
    mkdir -p hashcat/rules
    mkdir -p sources/words
    mkdir -p sources/rules
    mkdir -p sources/hashes
    mkdir -p outputs/hashcat
    mkdir -p tmp
fi
