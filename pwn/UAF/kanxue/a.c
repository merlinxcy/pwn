#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <dlfcn.h>
#include <stdint.h>
struct Message {
    int reply_count;
    struct Message* nextMsg;
    int msgid;
    char* author;
    int author_size;
    char* title;
    int title_size;
    char* content;
    int content_size;
    int total_num;
};
struct Message * head, *tail;
char input_buffer[0x1000];
void read_input(char * buf, int read_len, int buf_size) {
    if (NULL == buf || read_len <= 0)
        return;
    memset(buf, 0, buf_size);
    int i = 0;
    char temp_char;
    while (1) {
        temp_char = getchar();
        if (i < read_len)
            buf[i] = temp_char;
        if (temp_char == 0xA)
            break;
        i++;
    }
}
 
uint32_t read_input_uint(char *buf, int read_len, int buf_size) {
    read_input(buf, read_len, buf_size);
    return strtoul(buf, 0, 10);
}
void insertMessage(int messageId) {
    struct Message* tmp = head;
    while (tmp->nextMsg != tail) {
        tmp = tmp->nextMsg;
    }
 
    struct Message * new_msg;
    new_msg = (struct Message *) malloc(sizeof(struct Message));
    new_msg->msgid = messageId;
 
    write(STDOUT_FILENO, "input you name len:\n", 20);
    new_msg->author_size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    new_msg->author = (char *) malloc(new_msg->author_size);
    write(STDOUT_FILENO, "input you name:\n", 16);
    read_input(new_msg->author, new_msg->author_size, new_msg->author_size);
 
    write(STDOUT_FILENO, "input you title len:\n", 21);
    new_msg->title_size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    new_msg->title = (char *) malloc(new_msg->title_size);
    write(STDOUT_FILENO, "input you title:\n", 17);
    read_input(new_msg->title, new_msg->title_size, new_msg->title_size);
 
    write(STDOUT_FILENO, "input you content len:\n", 23);
    new_msg->content_size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    new_msg->content = (char *) malloc(new_msg->content_size);
    write(STDOUT_FILENO, "input you content:\n", 19);
    read_input(new_msg->content, new_msg->content_size, new_msg->content_size);
 
    new_msg->nextMsg = tmp->nextMsg;
    tmp->nextMsg = new_msg;
}
struct Message * print_msg(int msgid) {
    struct Message* tmp = head;
    while (tmp != tail) {
        if (tmp->msgid == msgid) {
            write(STDOUT_FILENO, "msg author:", 11);
            write(STDOUT_FILENO, tmp->author, tmp->author_size);
 
            write(STDOUT_FILENO, ",msg title:", 11);
            write(STDOUT_FILENO, tmp->title, tmp->title_size);
 
            write(STDOUT_FILENO, ",msg content:", 13);
            write(STDOUT_FILENO, tmp->content, tmp->content_size);
 
            //write(STDOUT_FILENO, ",msg reply count:", 17);
            //write(STDOUT_FILENO, tmp->reply_count, 4);
            write(STDOUT_FILENO, "\n", 1);
            /*printf(
             "\nmsg author:%s, msg title %s,msg content %s, msg reply count %d\n",
             tmp->author, tmp->title, tmp->content, tmp->reply_count);*/
            return tmp;
        }
        tmp = tmp->nextMsg;
    }
    return NULL;
}
void delete_msg(struct Message * delmsg) {
    //delete linked list msg and free
    struct Message* tmp = head;
    while (tmp->nextMsg != delmsg) {
        tmp = tmp->nextMsg;
    }
    tmp->nextMsg = delmsg->nextMsg;
    //free
    free(delmsg->author);
    free(delmsg->content);
    free(delmsg->title);
    free(delmsg);
}
void modify_msg(struct Message * modifymsg) {
    int size = 0;
    char temp[0x100];
 
    write(STDOUT_FILENO, "input new name len:\n", 20);
    size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    if (size > 0x100)
        return;
    write(STDOUT_FILENO, "input new name:\n", 16);
    read_input(temp, size, 0x100);
    memcpy(modifymsg->author, temp, size);
    modifymsg->author_size= size;
 
    write(STDOUT_FILENO, "input new title len:\n", 21);
    size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    if (size > 0x100)
        return;
    write(STDOUT_FILENO, "input new title:\n", 17);
    read_input(temp, size, 0x100);
    memcpy(modifymsg->title, temp, size);
    modifymsg->title_size= size;
 
    write(STDOUT_FILENO, "input new content len:\n", 23);
    size = read_input_uint(input_buffer, sizeof(input_buffer),
            sizeof(input_buffer));
    if (size > 0x100)
        return;
    write(STDOUT_FILENO, "input new content:\n", 19);
    read_input(temp, size, 0x100);
    modifymsg->content = (char *) malloc(size);
    memcpy(modifymsg->content, temp, size);
    modifymsg->content_size= size;
}
void main() {
    struct Message HEAD, TAIL;
    head = &HEAD;
    tail = &TAIL;
    head->nextMsg = tail;
    head->msgid = 0;
    tail->nextMsg = NULL;
    tail->msgid = -1;
 
    char usage[128] =
            "1.leave your message, 2.read the message,3.exit; please input you choice.\n";
    char operate_usage[80] =
            "Please select the operate: 1.delete 2.modify 3.add reply 4.back\n";
    int cmd = 0, msg_count = 0, operate = 0;
    while (1) {
        write(STDOUT_FILENO, usage, strlen(usage));
        read_input(input_buffer, sizeof(input_buffer), sizeof(input_buffer));
        sscanf(input_buffer, "%d", &cmd);
        switch (cmd) {
        case 1:             //添加留言
            msg_count++;
            insertMessage(msg_count);
            break;
        case 2:
            write(STDOUT_FILENO, "input msgid will read:\n", 23);
            int read_msg_id = 0;
            read_input(input_buffer, sizeof(input_buffer),
                    sizeof(input_buffer));
            sscanf(input_buffer, "%d", &read_msg_id);
            struct Message * read_msg = print_msg(read_msg_id);
            if (read_msg == NULL) {
                //write(STDOUT_FILENO, "msgid error\n", 12);
                return;
            }
            while (1) {
                write(STDOUT_FILENO, operate_usage, strlen(operate_usage));
                operate = read_input_uint(input_buffer, sizeof(input_buffer), sizeof(input_buffer));
                //sscanf(input_buffer, "%d", &operate);
                if (operate == 1) {
                    delete_msg(read_msg);
                } else if (operate == 2) {
                    modify_msg(read_msg);
                } else if (operate == 3) {
                    read_msg->reply_count++;
                } else if (operate == 4) {
                    break;
                }
 
            }
            break;
        case 3:
            write(STDOUT_FILENO, "exit\n", 5);
            return;
        }
    }
 
}
