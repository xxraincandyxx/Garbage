#include <functional>
#include <iostream>
#include <vector>

struct ttNode {
    // direct: left(0), up(1), right(2), down(3)
    int r, c;
    int direct;

    // for encode/decode:
    // fornt: F
    // left:  L
    // right: R
    ttNode* front;
    ttNode* left;
    ttNode* right;

    ttNode(int r, int c)
        : r(r), c(c), front(nullptr), left(nullptr), right(nullptr) {}
};

class TernaryTree {
   public:
    TernaryTree() : root(nullptr) {}

    void build(std::string& str_path) {
        insert_node(root, str_path, 0, 0, 0, 0);
    }

   private:
    ttNode* root;

    void insert_node(ttNode* node, std::string& str_path, int cur, int r, int c, int direct) {
        if (node == nullptr) node = new ttNode(r, c);
        if (str_path[cur] == '\0') return;
        if (str_path[cur] == 'F') {
            if (direct == 0) { c--; }
            if (direct == 1) { r--; }
            if (direct == 2) { c++; }
            if (direct == 3) { r++; }
            insert_node(node->front, str_path, cur + 1, r, c, direct);
        } else if (str_path[cur] == 'L') {
            if (direct == 0) { r++; direct=3; }
            if (direct == 1) { c--; direct=0; }
            if (direct == 2) { r--; direct=1; }
            if (direct == 3) { c++; direct=2; }
            insert_node(node->left, str_path, cur + 1, r, c, direct);
        } else {
            if (direct == 0) { r--; direct=1; }
            if (direct == 1) { c++; direct=2; }
            if (direct == 2) { r++; direct=3; }
            if (direct == 3) { c--; direct=0; }
            insert_node(node->right, str_path, cur + 1, r, c, direct);
        }
    }
};

int main(void) { return 0; }