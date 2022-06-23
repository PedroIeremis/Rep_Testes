#! /bin/bash

echo "Olá, tudo bem?"

read x

if [ $x = "sim" ];then
    echo "Ótimo!!"
else
    echo "Que peninha"
    echo "\nMas porque não tá bem?"
    read r
    echo "Nooouusaa..."
fi
