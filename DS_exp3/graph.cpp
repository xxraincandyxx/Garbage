#include <algorithm>
#include <functional>
#include <iostream>
#include <memory>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

class mGraph {
   public:
    mGraph(int n)
        : n(n),
          e(0),
          adj(new std::vector<std::vector<int>>(n, std::vector<int>(n, 0))) {}

    void destroy() {
        if (!adj) return;
        for (int i = 0; i < n; i++) adj->at(i).clear();
        adj->clear();
        delete adj;
        adj = nullptr;
        n = 0;
        e = 0;
    }

    void insert(int u, int v, int val = 1) {
        if (u < 0 || u >= n || v < 0 || v >= n) return;
        if ((*adj)[u][v] != 0 || (*adj)[v][u] != 0) return;
        (*adj)[u][v] = 1;
        (*adj)[v][u] = 1;
        e++;
    }

    void remove(int u, int v) {
        if (u < 0 || u >= n || v < 0 || v >= n) return;
        if ((*adj)[u][v] == 0 || (*adj)[v][u] == 0) return;
        (*adj)[u][v] = 0;
        (*adj)[v][u] = 0;
        e--;
    }

    bool exist(int u, int v) {
        if (u < 0 || u >= n || v < 0 || v >= n) return false;
        if ((*adj)[u][v] != 0 || (*adj)[v][u] != 0) return true;
        return false;
    }

    void _output() {
        std::cout << "Graph Adjacency Matrix: address & val" << std::endl;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++)
                std::cout << &(*adj)[i][j] << " " << (*adj)[i][j] << " ";
            std::cout << std::endl;
        }
    }

   private:
    int n, e;
    std::vector<std::vector<int>>* adj;
};

int main(void) {
    // initialize graph
    mGraph graph(5);

    graph.insert(0, 1);
    graph._output();

    std::cout << "is exist: " << graph.exist(0, 1) << std::endl;

    graph.remove(0, 1);
    graph._output();

    // destroy graph
    graph.destroy();
    return 0;
}
