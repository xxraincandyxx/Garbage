#include <algorithm>
#include <fstream>
#include <iostream>
#include <queue>
#include <sstream>
#include <string>
#include <unordered_map>
#include <vector>

class graph {
   public:
    // TODO: implement graph class
   private:
    int n, e;
    struct edge {
        int adj_vex, val;
        edge* nxt;
        edge(int adj_vex, int val) : adj_vex(adj_vex), val(val), nxt(nullptr) {}
    };
};
