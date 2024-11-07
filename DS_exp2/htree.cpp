// Huffman Tree
//
#include <iostream>
#include <queue>
#include <vector>
#include <unordered_map>
#include <memory>
#include <string>

struct hfNode {
    char ch;
    int weight;
    hfNode *left;
    hfNode *right;

    hfNode(char ch, int weight) : ch(ch), weight(weight), left(nullptr), right(nullptr) {}
};

class HuffmanTree {
public:
    HuffmanTree() : root(nullptr) {}

    void build(const std::unordered_map<char, int>& weight_map) {
        root = build_huffmantree(weight_map);
    }

    void preorder() const {
        if (root == nullptr) {
            std::cout << "None" << std::endl;
            return;
        }
        preorder_traversal(root);
        std::cout << std::endl;
    }

    void inorder() const {
        if (root == nullptr) {
            std::cout << "None" << std::endl;
            return;
        }
        inorder_traversal(root);
        std::cout << std::endl;
    }

    void postorder() const {
        if (root == nullptr) {
            std::cout << "None" << std::endl;
            return;
        }
        postorder_traversal(root);
        std::cout << std::endl;
    }

    void destroy() {
        rm_branch(root);
        root = nullptr;
    }

private:
    hfNode *root;

    void preorder_traversal(hfNode* node) const {
        if (node == nullptr) { return; }
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "Weight: " << node->weight << std::endl << std::endl;
        preorder_traversal(node->left);
        preorder_traversal(node->right);
    }

    void inorder_traversal(hfNode* node) const {
        if (node == nullptr) { return; }
        inorder_traversal(node->left);
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "Weight: " << node->weight << std::endl << std::endl;
        inorder_traversal(node->right);
    }

    void postorder_traversal(hfNode* node) const {
        if (node == nullptr) { return; }
        postorder_traversal(node->left);
        postorder_traversal(node->right);
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "Weight: " << node->weight << std::endl << std::endl;
    }

    void rm_branch(hfNode* node) {
        if (node == nullptr) { return; }
        rm_branch(node->left);
        rm_branch(node->right);
        delete node;
    }

    void build_huffmancode(const hfNode* root, std::string str, std::unordered_map<char, std::string> &code_map) {
        if (root == nullptr) { return; }
        if (root->left == nullptr && root->right == nullptr) {
            code_map[root->ch] = str;
        } else {
            build_huffmancode(root->left, str + "0", code_map);
            build_huffmancode(root->right, str + "1", code_map);
        }
    }

    hfNode* build_huffmantree(const std::unordered_map<char, int>& weight_map) {
        auto comp = [](const hfNode* a, const hfNode* b) { return a->weight > b->weight; };
        std::priority_queue<hfNode*, std::vector<hfNode*>, decltype(comp)> minHeap(comp);
        for (const auto& [ch, weight] : weight_map) {
            minHeap.push(new hfNode(ch, weight));
        }

        while (minHeap.size() > 1) {
            auto left = minHeap.top(); minHeap.pop();
            auto right = minHeap.top(); minHeap.pop();

            auto sum = new hfNode('\0', left->weight + right->weight);
            sum->left = left;
            sum->right = right;
            minHeap.push(sum);
        }
        return minHeap.top();
    }
};

int main(void) {
    HuffmanTree root;
    std::unordered_map<char, int> weights_map = {
        {'A', 5}, {'B', 9}, {'C', 12}, {'D', 13}, {'E', 16}, {'F', 45}
    };

    root.build(weights_map);
    root.preorder();
    // root.inorder();
    // root.postorder();
    root.destroy();

    return 0;
}
