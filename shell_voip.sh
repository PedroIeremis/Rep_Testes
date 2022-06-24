#!/bin/bash


res=$(curl -s "https://ipinfo.io/json" | tr -d "{" | cut -d ":" -f 2 | head -n 2 | tr -d '"' | tr -d ' ' | tr -d ',' | tr -d '\n')

echo $res
rm arq.sip
cp arq.sip.resv arq.sip
sed -i "s/ippublico/$res/" arq.sip
