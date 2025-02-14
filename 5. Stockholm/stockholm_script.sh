#!/bin/bash

mkdir -p /home/infection

extensions=(".der" ".pfx" ".key" ".crt" ".csr" ".p12" ".pem" ".odt" ".ott" ".sxw")
fake_extensions=(".xyz" ".abc" ".zzz" ".foo" ".bar")

create_file() {
    local file_path=$1
    echo "Ceci est un fichier avec l'extension $2." > "$file_path"
}

for ext in "${extensions[@]}"; do
    create_file "/home/infection/file$ext" "$ext"
done

for ext in "${fake_extensions[@]}"; do
    create_file "/home/infection/file$ext" "$ext"
done

echo "Les fichiers ont été créés dans /home/infection."
