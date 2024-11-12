#include <stdio.h>

void functionA() {
    printf("In functionA\n");
}

void functionB() {
    printf("In functionB\n");
}

void functionC() {
    printf("In functionC\n");
}

int main() {
    int condition1;
    int condition2;
    scanf("%d", &condition1);
    scanf("%d", &condition2);
    if (condition1==1) {
        functionA();
        if (condition2==0) {
            functionB();
        } else {
            functionC();
        }
    }
    return 0;
}
