#include<stdio.h>
#include<stdlib.h>
#include"BPfilter.h"

int main (void) {
    int i = 0;
    FILE* datus;
    FILE* writer;
    char buffer;
    char filename[100];
    printf("enter file name: ");
    scanf("%s",filename);
    datus = fopen(filename,"r");
    writer = fopen("filtered.csv","w");
    while (i < 72000) {
        int number = 0;
        int neg = 1;
        for(int j = 0;; j++) {
            buffer= getc(datus);
            if(buffer == '-') {
                neg = -1;
                continue;
            } else if(buffer == ',') break;
            number = number*10 + buffer - '0';
        }
        number *= neg;
        fprintf(writer, "%d", oBPfilterFS500(number, 2));
        if(i < 71999) fprintf(writer,",");
        i++;
    }
    fclose(datus);
    fclose(writer);
}
