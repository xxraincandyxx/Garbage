// Binary Tree Experiment
//
#include <iostream>

struct btNode {
    int elem;
    btNode* left;
    btNode* right;

    btNode(int val) : elem(val), left(nullptr), right(nullptr) {}
};

class BinaryTree {
   public:
    BinaryTree() : root(nullptr) {}

    void insert(int val) { root = insert_node(root, val); }

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

    void self_destruction() {
        rm_branch(root);
        root = nullptr;
    }

    int count_leaves() const {
        if (root == nullptr) {
            return 0;
        }
        return count_branch_leaves(root);
    }

    int count_nodes() const {
        if (root == nullptr) {
            return 0;
        }
        return count_branch_nodes(root);
    }

    int cal_depth() const {
        if (root == nullptr) {
            return 0;
        }
        return cal_branch_depth(root);
    }

    void swap_lr_branch() {
        if (root == nullptr) {
            return;
        }
        swap_branch(root);
    }

   private:
    btNode* root;

    void preorder_traversal(btNode* node) const {
        if (node == nullptr) {
            return;
        }
        std::cout << node->elem << ' ';
        preorder_traversal(node->left);
        preorder_traversal(node->right);
    }

    void inorder_traversal(btNode* node) const {
        if (node == nullptr) {
            return;
        }
        inorder_traversal(node->left);
        std::cout << node->elem << ' ';
        inorder_traversal(node->right);
    }

    void postorder_traversal(btNode* node) const {
        if (node == nullptr) {
            return;
        }
        postorder_traversal(node->left);
        postorder_traversal(node->right);
        std::cout << node->elem << ' ';
    }

    void rm_branch(btNode* node) {
        if (node == nullptr) {
            return;
        }
        rm_branch(node->left);
        rm_branch(node->right);
        delete node;
    }

    int count_branch_leaves(btNode* node) const {
        if (node == nullptr) {
            return 0;
        }
        if (node->left == nullptr && node->right == nullptr) {
            return 1;
        }
        return count_branch_leaves(node->left) +
               count_branch_leaves(node->right);
    }

    int count_branch_nodes(btNode* node) const {
        if (node == nullptr) {
            return 0;
        }
        return count_branch_nodes(node->left) +
               count_branch_nodes(node->right) + 1;
    }

    int cal_branch_depth(btNode* node) const {
        if (node == nullptr) {
            return 0;
        }
        return std::max(cal_branch_depth(node->left),
                        cal_branch_depth(node->right)) +
               1;
    }

    void swap_branch(btNode* node) {
        if (node == nullptr) {
            return;
        }
        swap_branch(node->left);
        swap_branch(node->right);
        std::swap(node->left, node->right);
        return;
    }

    btNode* insert_node(btNode* node, int val) {
        if (node == nullptr) {
            return new btNode(val);
        }
        if (val < node->elem) {
            node->left = insert_node(node->left, val);
        } else {
            node->right = insert_node(node->right, val);
        }
        return node;
    }
};

int main(void) {
    BinaryTree tree;

    tree.insert(4);
    tree.insert(2);
    tree.insert(6);
    tree.insert(1);
    tree.insert(3);
    tree.insert(5);
    tree.insert(7);

    std::cout << "Preorder Traversal: " << std::endl;
    tree.preorder();
    std::cout << "Inorder Traversal: " << std::endl;
    tree.inorder();
    std::cout << "Postorder Traversal: " << std::endl;
    tree.postorder();

    std::cout << "Number of Leaves: " << std::endl;
    int num_leaves = tree.count_leaves();
    std::cout << num_leaves << std::endl;

    std::cout << "Number of Nodes: " << std::endl;
    int num_nodes = tree.count_nodes();
    std::cout << num_nodes << std::endl;

    std::cout << "Depth of Tree: " << std::endl;
    int depth = tree.cal_depth();
    std::cout << depth << std::endl;

    tree.swap_lr_branch();
    std::cout << "Symetric of Tree: " << std::endl;
    tree.preorder();

    tree.self_destruction();
    return 0;
}
