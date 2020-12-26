#include <stdio.h>
#include <string.h>
#include <unistd.h>
#define BUFSIZE1 1020
#define BUFSIZE2 ((BUFSIZE1/2) - 4)
int main(int argc, char **argv) {
 char* name = malloc(12); /* [1] */
 char* details = malloc(12); /* [2] */
 strncpy(name, argv[1], 12-1); /* [3] */
 free(details); /* [4] */
 free(name);  /* [5] */
 printf("Welcome %s\n",name); /* [6] */
 fflush(stdout);
 char* tmp = (char *) malloc(12); /* [7] */
 char* p1 = (char *) malloc(BUFSIZE1); /* [8] */
 char* p2 = (char *) malloc(BUFSIZE1); /* [9] */
 free(p2); /* [10] */
 char* p2_1 = (char *) malloc(BUFSIZE2); /* [11] */
 char* p2_2 = (char *) malloc(BUFSIZE2); /* [12] */
 printf("Enter your region\n");
 fflush(stdout);
 read(0,p2,BUFSIZE1-1); /* [13] */
 printf("Region:%s\n",p2); 
 free(p1); /* [14] */
}
