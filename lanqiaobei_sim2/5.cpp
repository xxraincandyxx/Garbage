#include <algorithm>
#include <cstring>
#include <functional>
#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    std::vector<int> arr = {
        2238, 386, 319, 692, 169, 338, 521, 713, 640, 692, 969, 362, 311, 349,
        308,  357, 515, 140, 591, 57,  252, 575, 630, 95,  274, 328, 614, 18,
        605,  17,  980, 166, 112, 997, 37,  584, 64,  442, 495, 821, 459, 453,
        597,  187, 734, 827, 950, 679, 78,  769, 661, 452, 983, 356, 217, 394,
        342,  697, 878, 475, 250, 468, 33,  966, 742, 436, 343, 255, 944, 588,
        734,  540, 508, 779, 881, 153, 928, 764, 703, 459, 949, 500, 163, 547,
        780,  749, 132, 546, 199, 701, 448, 265, 263, 87,  45,  828, 634};
    int max_sum = arr[0];
    for (int i = 1; i < arr.size(); i++) {
        for (int j = i + 1; j < arr.size(); j++) {
            if (max_sum + arr[j])
        }
    }
    std::cout << std::endl << max_sum << std::endl;
    return 0;
}