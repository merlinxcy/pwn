/* uaf.c */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct Box {
    int size;
    char *buf;
};

struct Box *create_box(int size)
{
    struct Box *box;
    box = malloc(sizeof(struct Box));
    box->size = size;
    box->buf = malloc(size);
    return box;
}

void free_box(struct Box *box)
{
    free(box->buf);
    free(box);
}

int main(int argc, char *argv[])
{
    struct Box *box;
    int size;
    char *newbuf;
    int test;

    scanf("%d", &test); //stop the program for debugging

    box = create_box(100);
    printf("[+] box = %p\n", box);
    strncpy(box->buf, argv[1], 100);
    printf("[+] box->buf = %p\n", box->buf);
    free_box(box);

    size = atoi(argv[2]);
    newbuf = malloc(size);
    printf("[+] newbuf = %p\n", newbuf);
    strncpy(newbuf, argv[3], size);
    printf("[+] box->buf = %p\n", box->buf);

    strncpy(box->buf, argv[4], 100);
    printf("[+] *box->buf = 0x%x\n", ((int*)(box->buf))[0]);

    free(newbuf);
    return 0;
}
