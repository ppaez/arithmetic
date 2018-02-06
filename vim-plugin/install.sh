#! /bin/bash

SOURCE=$(dirname $0)
DEST_PLUGIN=$HOME/.vim/plugin/arithmetic
DEST_DOC=$HOME/.vim/doc/arithmetic
DEST_PYTHON3=$HOME/.vim/python3

mkdir -p $DEST_PLUGIN
mkdir -p $DEST_DOC
mkdir -p $DEST_PYTHON3

echo Installing the arithmetic plugin
cp -avf $SOURCE/arithmetic.vim $DEST_PLUGIN
cp -avf $SOURCE/arithmetic.txt $SOURCE/tutorial.txt $DEST_DOC
cp -avf $SOURCE/wrapper.py $DEST_PYTHON3

echo Prepare :help arithmetic
if vim --not-a-term --noplugin --cmd ':helptags $HOME/.vim/doc' --cmd ':quit' > /dev/null; then
    echo Ok
else
    echo Failed
fi

echo Check the Python arithmetic module
pushd /tmp > /dev/null
if python3 -u -c 'import arithmetic' > /dev/null 2>&1; then
    echo Ok
else
    echo Missing. Run the command \"su -c 'python3 setup.py install'\" to install it
fi
popd > /dev/null
echo Done
