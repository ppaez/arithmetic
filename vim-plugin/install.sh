#! /bin/bash

SOURCE=$(dirname $0)
DEST_PLUGIN=$HOME/.vim/plugin
DEST_DOC=$HOME/.vim/doc/arithmetic
DEST_PYTHON3=$HOME/.vim/python3

mkdir -p $DEST_PLUGIN
mkdir -p $DEST_DOC
mkdir -p $DEST_PYTHON3

echo Installing the arithmetic plugin -------

echo Check that Vim includes Python 3 support
if vim --version | grep +python3 > /dev/null; then
    echo Ok
else
    echo Missing. In Debian, run the command \"apt install vim-nox\"
    echo or \"apt install vim-gtk3\" to include Python 3 support
    exit 1
fi

echo Copy files under ~/.vim
cp -avf $SOURCE/arithmetic.vim $DEST_PLUGIN
cp -avf $SOURCE/arithmetic.txt $SOURCE/tutorial.txt $DEST_DOC
cp -avf $SOURCE/wrapper.py $DEST_PYTHON3
cp -avf $SOURCE/../arithmetic.py $DEST_PYTHON3
echo Ok

echo Prepare :help arithmetic
if vim --not-a-term --noplugin --cmd ':helptags $HOME/.vim/doc' --cmd ':quit' > /dev/null; then
    echo Ok
else
    echo Failed
fi

echo Finished ------------------------------
