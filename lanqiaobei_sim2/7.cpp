#include <iostream>
#include <vector>

int main(void) {
    int n;
    std::vector<int> arr = {};
    std::cin >> n;
    for (int i = 0; i < n; i++) {
        int val;
        std::cin >> val;
        arr.push_back(val);
    }

    int min_even = INT_MAX;
    for (auto val : arr) {
        if (val % 2 == 0 && val < min_even) min_even = val;
    }
    std::cout << min_even << std::endl;
    return 0;
}