#include <stdio.h>

int functionB(int x) {
    printf("In functionB with parameter x = %d\n", x);
    return x * 2;
}

void functionA(double y) {
    int result = functionB(10);
    printf("Result from functionB: %d\n", result);
}

int main() {
    printf("In main\n");
    functionA(5.5);
    return 0;
}
