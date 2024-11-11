#include <stdio.h>

void functionD() {
    printf("In functionD\n");
}

int functionC(int x) {
    printf("In functionC with x = %d\n", x);
    return x + 1;
}

void functionB(double y) {
    int result = functionC(5);
    printf("Result from functionC: %d\n", result);
}

void functionA() {
    functionB(2.0);
    functionD();
}

int main() {
    printf("In main\n");
    functionA();
    return 0;
}
