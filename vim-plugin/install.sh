#! /bin/bash

SOURCE=$(dirname $0)
DEST_PLUGIN=$HOME/.vim/plugin/arithmetic
DEST_DOC=$HOME/.vim/doc/arithmetic
DEST_PYTHON3=$HOME/.vim/python3

mkdir -p $DEST_PLUGIN
mkdir -p $DEST_DOC
mkdir -p $DEST_PYTHON3

cp -avf $SOURCE/arithmetic.vim $DEST_PLUGIN
cp -avf $SOURCE/arithmetic.txt $SOURCE/tutorial.txt $DEST_DOC
cp -avf $SOURCE/wrapper.py $DEST_PYTHON3

vim --noplugin --cmd ':helptags $HOME/.vim/doc' --cmd ':quit'
