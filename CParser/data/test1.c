#include <stdio.h>

void functionA(int x, int y, int z) {
    printf("In functionA with parameter x = %d\n", x);
}

int main() {
    printf("In main\n");
    functionA(5, 6, 7);
    return 0;
}
