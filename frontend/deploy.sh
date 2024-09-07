HTML_DIR=~/Documents/Programowanie/matlewan/matlewan.github.io
DIR=$HTML_DIR/pomysl-grandprix
mkdir -p $DIR
rm -rf $DIR/*
cp -r ./dist/* $DIR
code $HTML_DIR
