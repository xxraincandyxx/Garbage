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
        (*adj)[u][v] = val;
        (*adj)[v][u] = val;
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

    void depth_first_search(int val) {
        std::vector<bool> visited(n, false);
        std::function<void(int)> dfs = [&](int u) {
            visited[u] = true;
            for (int v = 0; v < n; v++) {
                if (!adj->at(u)[v] || visited[v]) continue;
                dfs(v);
            }
            std::cout << u << " ";
        };
        std::cout << "depth first search from [" << val << "]: " << std::endl;
        dfs(val);
        visited.clear();
    }

    void breadth_first_search(int val) {
        std::vector<bool> visited(n, false);
        std::queue<int> q;
        std::cout << "breadth first search from [" << val << "]: " << std::endl;
        q.push(val);
        visited[val] = true;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            std::cout << u << " ";
            for (int v = 0; v < n; v++) {
                if (!adj->at(u)[v] || visited[v]) continue;
                q.push(v);
                visited[v] = true;
            }
        }
    }

    void shortest_path(int val) {
        std::vector<int> dist(n, INT_MAX);
        std::vector<int> prev(n, -1);
        std::vector<bool> visited(n, false);
        std::function<void(int)> dfs = [&](int u) {
            visited[u] = true;
            for (int v = 0; v < n; v++) {
                if (!adj->at(u)[v] || visited[v]) continue;
                dist[v] = std::min(dist[v], dist[u] + adj->at(u)[v]);
                prev[v] = u;
                dfs(v);
            }
        };
        std::cout << "shortest path from [" << val << "]: " << std::endl;
        dfs(val);
        for (int i = 0; i < n; i++) {
            if (dist[i] == INT_MAX) continue;
            std::cout << "to " << i << ": " << dist[i] << std::endl;
        }
    }

   private:
    int n, e;
    std::vector<std::vector<int>>* adj;
};

int main(void) {
    // initialize graph
    mGraph graph(4);

    // insert edges
    graph.insert(0, 1, 1);
    graph.insert(1, 1, 2);
    graph.insert(1, 2, 3);
    graph.insert(1, 1, 4);
    graph.insert(3, 2, 5);
    graph.insert(3, 3, 6);

    graph._output();
    std::cout << std::endl;

    // check exist
    std::cout << "is (0, 1) exist: " << graph.exist(0, 1) << std::endl;
    std::cout << "is (0, 0) exist: " << graph.exist(0, 0) << std::endl;

    // remove edges
    std::cout << std::endl;
    graph.remove(0, 1);
    std::cout << "remove (0, 1)" << std::endl;
    graph.remove(3, 3);
    std::cout << "remove (3, 3)" << std::endl;

    graph._output();
    std::cout << std::endl;

    // depth-first search
    graph.depth_first_search(0);
    std::cout << std::endl;
    graph.depth_first_search(1);

    std::cout << std::endl << std::endl;

    // breath-first search
    graph.breadth_first_search(0);
    std::cout << std::endl;
    graph.breadth_first_search(1);

    // destroy graph
    graph.destroy();
    return 0;
}
