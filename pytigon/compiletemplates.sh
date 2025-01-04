#!/bin/bash

for dir in prj/*/ ; do
    if [ -d "$dir" ]; then
        folder_name=$(basename "${dir%/}")
        #if [ "$folder_name" == "_schall" ]; then
        #    continue
        #fi
        echo ptig manage_$folder_name compiletemplates
        pptig --dev manage_$folder_name compiletemplates
    fi
done
