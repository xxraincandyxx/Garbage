#include <iostream>

int main(void) {
    int n = 0;
    std::cin >> n;
    if (2024 % n == 0)
        std::cout << 2024 / n << std::endl;
    else
        std::cout << 2024 / n + 1 << std::endl;
    return 0;
}