import vim
from arithmetic import Parser


def calculate():
    'Parse and evaluate the current buffer and return a status'

    buffer = vim.current.buffer

    text = '\n'.join(buffer)

    parser = Parser()
    result = parser.parse(text)
    
    for i, line in enumerate(result.splitlines()):
        vim.current.buffer[i] = line

    return "{} lines in current buffer".format(len(buffer))
