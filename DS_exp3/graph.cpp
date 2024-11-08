#include <algorithm>
#include <functional>
#include <iostream>
#include <memory>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

class Graph {
   public:
    Graph(int n)
        : n(n),
          e(0),
          adj(new std::vector<std::vector<int>>(n, std::vector<int>(n, 0))) {}
    
    void add_edge(int u, int v) {
        if (u < 0 || u >= n || v < 0 || v >= n) return;
        (*adj)[u][v] = 1;
        (*adj)[v][u] = 1;
        e++;
    } // TODO: More Implemetations

   private:
    int n, e;
    std::vector<std::vector<int>>* adj;
};

int main(void) { return 0; }
