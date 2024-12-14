#include <algorithm>
#include <cstring>
#include <functional>
#include <iostream>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

int main() {
    auto get_max_digit = [&](int val) {
        int res = 0;
        while (val) {
            if (val % 10 > res) res = val % 10;
            val /= 10;
        }
        return res;
    };
    // std::cout << get_max_digit(1) << std::endl;

    int tar = 2024;
    int wei_max = tar * 10 - 1;
    int val_max = tar;
    std::vector<std::vector<bool>> vis(tar + 1,
                                       std::vector<bool>(tar * 10, false));
    std::function<void(int, int)> dfs = [&](int val, int wei) {
        if (val > val_max || wei > wei_max) return;
        if (vis[val][wei]) return;
        vis[val][wei] = true;
        if (val >= tar) return;
        dfs(val + 1, wei + 1);
        dfs(val + get_max_digit(val), wei + 3);
        dfs(val * 2, wei + 10);
        return;
    };

    dfs(1, 0);
    for (int i = 0; i < vis[tar].size(); i++) {
        if (vis[tar][i]) {
            std::cout << i << std::endl;
            return 0;
        }
    }
    std::cout << "failed" << std::endl;
    return 0;
}