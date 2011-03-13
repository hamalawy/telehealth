#include <stdio.h>
#include <stdlib.h>
#include"BPfilter.h"

using namespace std;

int main (void) {
    char buffer;
    while (true) {
        int number = 0;
        int neg = 1;
        while(true) {
            buffer = getchar();
            if(buffer == '-') neg = -1;
            else if(buffer >= '0' && buffer <= '9') number = number*10 + buffer - '0';
            else if(buffer == ',') break;
            else if(buffer == '*') goto stop;
            else continue;
        }
        number *= neg;
        printf("%d,",oBPfilterFS500(number, 2));
    }
    stop:
    return 0;
}
