#include <iostream>
#include <functional>
#include <vector>
#include <queue>

struct btNode {
    int val;
    btNode* left;
    btNode* right;

    btNode(int val)
        : val(val), left(nullptr), right(nullptr) {}
};

class MinHeap {
   public:
    MinHeap() : root(nullptr) {}

    void build(const std::vector<int>& arr) {
        for (auto val : arr) { _insert(val); }
    }

    void push(int val) {
        if (root == nullptr) { return; }
        _insert(val);
    }

    int pop() { return _delete(); }

    void clear() {
        _clear();
    }

   private:
    btNode* root;

    void _insert(int val) { root = _insert_node(root, val); }

    int _delete() {
        if (root == nullptr) { return -1; }
        return _delete_min_node(root);
    }

    void _clear() {
        _recur_clear(root);
    }

    void _recur_clear(btNode* node) {
        if (node == nullptr) { return; }
        _recur_clear(node->left);
        _recur_clear(node->right);
        delete node;
        node = nullptr;
    }

    int _delete_min_node(btNode* node, btNode* parent = nullptr) {
        if (node == nullptr) { return -1; }
        if (node->left == nullptr) {
            int val = node->val;
            if (node->right != nullptr) {
                parent->left = node->right;
                delete node;
                node = nullptr;
                return val;
            }
            delete node;
            node = nullptr;
            if (parent != nullptr) parent->left = nullptr;
            return val;
        }
        return _delete_min_node(node->left, node);
    }

    btNode* _insert_node(btNode* node, int val) {
        if (node == nullptr) { return new btNode(val); }
        if (val < node->val) {
            node->left = _insert_node(node->left, val);
        } else {
            node->right = _insert_node(node->right, val);
        }
        return node;
    }
};

class algo {
   public:
	algo(std::vector<int> seq) : seq(seq), bkup(seq) {}

	void _output() {
		std::cout << "seq vals: " << std::endl;
		for (auto val : seq) { std::cout << val << " "; }
		std::cout << std::endl;
	}

	void _restore() {
		for (int i = 0; i < seq.size(); i++) { seq[i] = bkup[i]; }
	}

	void csort() {
		int k = 0;
		for (int i = 0; i < seq.size() - 1; i++) {
			k = i;
			for (int j = i + 1; j < seq.size(); j++)
				if (seq[j] < seq[k]) { k = j; }
			std::swap(seq[i], seq[k]);
		}
	}

	void isort() {
	    	for (int i = 0; i < seq.size() - 1; i++) {
                int j = i + 1;
                for (int k = j - 1; k >= 0; k--)
                    if (seq[k] > seq[k+1]) {  std::swap(seq[k], seq[k+1]); }
            }
	}

	void bsort() {
		for (int i = 0; i < seq.size() - 1; i++)
			for (int j = i + 1; j < seq.size(); j++)
				if (seq[j] < seq[i]) { std::swap(seq[i], seq[j]); }
	}

    void qsort() {
        std::function<void(int, int)> qs = [&](int lef, int rig) {
            if (lef >= rig) { return; }
            int pivot = seq[rig], i = lef - 1;
            for (int j = lef; j < rig; j++)
                if (seq[j] <= pivot)
                    std::swap(seq[++i], seq[j]);
            std::swap(seq[++i], seq[rig]);
            qs(lef, i - 1);
            qs(i + 1, rig);
        };
        qs(0, seq.size() - 1);
    }

    void msort() {
        std::function<void(int, int, int)> merge = [&](int lef, int mid, int rig) {
            int ln = mid - lef + 1, rn = rig - mid;
            std::vector<int> left(ln);
            std::vector<int> right(rn);

            // clone seq to left, right
            for (int i = 0; i < ln; i++)
                left[i] = seq[lef + i];
            for (int i = 0; i < rn; i++)
                right[i] = seq[mid + 1 + i];

            // merge
            int i = 0, j = 0, k = lef;
            while(i < ln && j < rn) {
                if(left[i] <= right[j]) {
                    seq[k] = left[i];
                    i++;
                } else {
                    seq[k] = right[j];
                    j++;
                }
            k++;
            }
            while(i < ln) {
                seq[k] = left[i];
                i++;
                k++;
            }
            while(j < rn) {
                seq[k] = right[j];
                j++;
                k++;
            }
        };

        std::function<void(int, int)> ms = [&](int lef, int rig) {
            if (lef >= rig) { return; }
            int mid = lef + ((rig - lef) >> 1);

            ms(lef, mid);
            ms(mid + 1, rig);

            merge(lef, mid, rig);
        };

        ms(0, seq.size() - 1);
    }

    void hsort() {
        auto comp = [](const int& a, const int& b) { return a > b; };
        std::priority_queue<int, std::vector<int>, decltype(comp)> heap(comp);
        for (auto val : seq) { heap.push(val); }
        for (int i = 0; i < seq.size(); i++) {
            seq[i] = heap.top();
            heap.pop();
        }
    }

    void fhsort() {
        MinHeap min_heap;
        min_heap.build(seq);
        for (int i = 0; i < seq.size(); i++) {
            seq[i] = min_heap.pop();
        }
    }

   private:
	std::vector<int> seq;
	std::vector<int> bkup;
};

int main(void) {
	algo seq({5, 4, 3, 2, 1});
	seq._output();

	// simple chosen sort
	seq.csort();
    std::cout << "chosen sort -> ";
	seq._output();
	seq._restore();

    // insertion sort
    seq.isort();
    std::cout << "insert sort -> ";
    seq._output();
    seq._restore();

	// buble sort
	seq.bsort();
    std::cout << "buble sort -> ";
	seq._output();
	seq._restore();

    // quick sort
    seq.qsort();
    std::cout << "quick sort -> ";
    seq._output();
    seq._restore();

    // merge sort
    seq.msort();
    std::cout << "merge sort -> ";
    seq._output();
    seq._restore();

    // heap sort
    seq.hsort();
    std::cout << "heap sort -> ";
    seq._output();
    seq._restore();

    // fast heap sort
    seq.fhsort();
    std::cout << "fast heap sort -> ";
    seq._output();
    seq._restore();

	return 0;
}

