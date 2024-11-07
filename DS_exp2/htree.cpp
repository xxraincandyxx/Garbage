// Huffman Tree
//
#include <iostream>
#include <memory>
#include <queue>
#include <string>
#include <unordered_map>
#include <vector>

struct hfNode {
    char ch;
    int freq;
    hfNode* left;
    hfNode* right;

    hfNode(char ch, int freq)
        : ch(ch), freq(freq), left(nullptr), right(nullptr) {}
};

class HuffmanTree {
   public:
    HuffmanTree() : root(nullptr) {}

    void build(const std::unordered_map<char, int>& freq_map) {
        root = build_huffmantree(freq_map);
        build_codemap(root, "", codemap);
    }

    std::string encode(const std::string& text) {
        if(codemap.empty() || !root) return "";
        return encoder(text);
    }

    std::string decode(const std::string& code) {
        if(codemap.empty() || !root) return "";
        std::string text = "";
        decoder(root, code, text, 0);
        return text;
    }

    void output_codemap() {
        if(codemap.empty()) {
            std::cout << "None" << std::endl;
            return;
        }
        for(const auto& [ch, str] : codemap) {
            std::cout << "Character: " << ch << " Code: " << str << std::endl;
        }
    }

    void preorder() const {
        if(root == nullptr) {
            std::cout << "None" << std::endl;
            return;
        }
        preorder_traversal(root);
        std::cout << std::endl;
    }

    void inorder() const {
        if(root == nullptr) {
            std::cout << "None" << std::endl;
            return;
        }
        inorder_traversal(root);
        std::cout << std::endl;
    }

    void postorder() const {
        if(root == nullptr) {
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
    hfNode* root;
    std::unordered_map<char, std::string> codemap;

    void preorder_traversal(hfNode* node) const {
        if(node == nullptr) return;
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "freq: " << node->freq << std::endl << std::endl;
        preorder_traversal(node->left);
        preorder_traversal(node->right);
    }

    void inorder_traversal(hfNode* node) const {
        if(node == nullptr) return;
        inorder_traversal(node->left);
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "freq: " << node->freq << std::endl << std::endl;
        inorder_traversal(node->right);
    }

    void postorder_traversal(hfNode* node) const {
        if(node == nullptr) return;
        postorder_traversal(node->left);
        postorder_traversal(node->right);
        std::cout << "Character: " << node->ch << ' ' << std::endl;
        std::cout << "Frequency: " << node->freq << std::endl << std::endl;
    }

    void rm_branch(hfNode* node) {
        if(node == nullptr) return;
        rm_branch(node->left);
        rm_branch(node->right);
        delete node;
    }

    void build_codemap(const hfNode* node, std::string str,
                       std::unordered_map<char, std::string>& code_map) {
        if(node == nullptr) return;
        if(node->left == nullptr && node->right == nullptr) {
            code_map[node->ch] = str;
        } else {
            build_codemap(node->left, str + "0", code_map);
            build_codemap(node->right, str + "1", code_map);
        }
    }

    hfNode* build_huffmantree(const std::unordered_map<char, int>& freq_map) {
        auto comp = [](const hfNode* a, const hfNode* b) {
            return a->freq > b->freq;
        };
        std::priority_queue<hfNode*, std::vector<hfNode*>, decltype(comp)>
            minHeap(comp);
        for(const auto& [ch, freq] : freq_map)
            minHeap.push(new hfNode(ch, freq));

        while(minHeap.size() > 1) {
            auto left = minHeap.top();
            minHeap.pop();
            auto right = minHeap.top();
            minHeap.pop();

            auto sum = new hfNode('\0', left->freq + right->freq);
            sum->left = left;
            sum->right = right;
            minHeap.push(sum);
        }
        return minHeap.top();
    }

    std::string encoder(std::string text) {
        if(codemap.empty() || !root) return "";
        std::string code = "";
        for(char ch : text) code += codemap[ch];
        return code;
    }

    void decoder(const hfNode* node, const std::string& code, std::string& text,
                 int cur) {
        if(node->left == nullptr && node->right == nullptr) {
            text += node->ch;
            decoder(root, code, text, cur);
            return;
        }
        if(code[cur] == '\0') return;
        if(code[cur] == '0') {
            decoder(node->left, code, text, cur + 1);
        } else if(code[cur] == '1') {
            decoder(node->right, code, text, cur + 1);
        }
        return;
    }
};

int main(void) {
    HuffmanTree root;
    std::unordered_map<char, int> freq_map = {{'A', 5},  {'B', 9},  {'C', 12},
                                              {'D', 13}, {'E', 16}, {'F', 45}};

    root.build(freq_map);
    root.preorder();
    // root.inorder();
    // root.postorder();

    std::cout << "Codemap:" << std::endl;
    root.output_codemap();
    std::string text = "ABCDEF";
    std::string code = root.encode(text);
    std::cout << "Encoded: " << code << std::endl;
    std::cout << "Decoded: " << root.decode(code) << std::endl;

    root.destroy();

    return 0;
}
