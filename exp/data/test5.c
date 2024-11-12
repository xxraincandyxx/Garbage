#include <stdio.h>

int functionB(int x) {
    printf("In functionB with x = %d\n", x);
    return x * 2;
}

void functionA(int y) {
    if (y > 5) {
        int result = functionB(y);
        printf("Result from functionB: %d\n", result);
    } else {
        printf("y is too small for functionB\n");
    }
}

int main() {
int value ;
scanf("%d", &value);
    if (value > 0) {
        functionA(value);
    } else {
        printf("Value is non-positive\n");
    }
    return 0;
}
