#! /bin/bash

SOURCE=$(dirname $0)
DEST_PLUGIN=$HOME/.vim/plugin/arithmetic
DEST_DOC=$HOME/.vim/doc/arithmetic

mkdir -p $DEST_PLUGIN
mkdir -p $DEST_DOC

cp -avf $SOURCE/arithmetic.vim $SOURCE/wrapper.py $DEST_PLUGIN
cp -avf $SOURCE/arithmetic.txt $SOURCE/tutorial.txt $DEST_DOC

vim --noplugin --cmd ':helptags $HOME/.vim/doc' --cmd ':quit'