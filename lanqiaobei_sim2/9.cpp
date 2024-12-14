#include <functional>
#include <iostream>
#include <vector>

void show_map(std::vector<std::vector<int>> map) {
    for (int h = 0; h < map.size(); h++)
        for (int w = 0; w < map[h].size(); w++) std::cout << map[h][w];
}

int main(void) {
    int height, width;
    std::cin >> height >> width;
    std::vector<std::vector<int>> map(height, std::vector<int>(width, 0));
    for (int h = 0; h < height; h++)
        for (int w = 0; w < width; w++)
            std::cin >> map[h][w];

    // w and h, all inclusive
    std::function<int(int, int, int, int)> get_sum = [&](int h1, int w1, int h2,
                                                         int w2) {
        int sum = 0;
        if (h1 != h2) {
            for (int w = w1; w <= w2; w++) sum += map[h1][w] + map[h2][w];
            for (int h = h1 + 1; h <= h2 - 1; h++)
                sum += map[h][w1] + map[h][w2];
            return sum;
        } else {
            for (int w = w1; w <= w2; w++) sum += map[h1][w];
            return sum;
        }
    };

    int ch1, cw1, ch2, cw2;
    int max_sum = 0;
    int h1, w1, h2, w2;
    for (h1 = 0; h1 < height - 1; h1++) {
        for (w1 = 0; w1 < width - 1; w1++) {
            for (h2 = h1 + 1; h2 < height; h2++) {
                for (w2 = w1 + 1; w2 < width; w2++) {
                    if (h2 - h1 != w2 - w1) continue;
                    int sum = get_sum(h1, w1, h2, w2);
                    if (sum > max_sum) {
                        ch1 = h1;
                        ch2 = h2;
                        cw1 = w1;
                        cw2 = w2;
                        max_sum = sum;
                    }
                }
            }
        }
    }

    std::cout << max_sum;
    return 0;
}
// std::cout << std::endl << ch1 << cw1 << ch2 << cw2;
// Deprecated
// std::vector<std::vector<std::vector<std::vector<bool>>>> vis(
//     height, std::vector<std::vector<std::vector<bool>>>(
//                 width, std::vector<std::vector<bool>>(
//                            height, std::vector<bool>(width, false))));

// std::function<int(int, int, int, int)> dfs = [&](int h1, int w1, int h2,
//                                                  int w2) {
//     if (vis[h1][w1][h2][w2]) return 0;
//     vis[h1][w1][h2][w2] = true;
//     if (  // reach frontier
//         h1 < 0 || h1 >= height || h2 < 0 || h2 >= height || w1 < 0 ||
//         w1 >= width || w2 < 0 || w2 >= width || h1 > h2 || w1 > w2) {
//         return 0;
//     }
//     return std::max(
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2),
//         dfs(h1, w1, h2, w2) // TODO
//     );
// };