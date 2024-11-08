#include <iostream>
#include <vector>

// Linear Array
//
typedef struct seq {
    int n;
    int cur;
    int* elem;
} Seq;

void _init(Seq* a, int n) {
    a->n = n;     // exclusive
    a->cur = -1;  // inclusive
    a->elem = (int*)malloc(n * sizeof(int));
}

int _find(Seq* a, int val) {
    for (int i = 0; i <= a->cur; i++)
        if (a->elem[i] == val) return i;
    return -1;  // failure
}

int _insert(Seq* a, int idx, int val) {
    if (idx < 0 || idx > a->n) {
        return -1;
    }  // index error
    if (a->cur >= a->n - 1) {
        return -1;
    }  // alloc error
    for (int j = a->cur + 1; j > idx; j--) {
        // swap elem
        a->elem[j - 1] = a->elem[j] ^ a->elem[j - 1];
        a->elem[j] = a->elem[j - 1] ^ a->elem[j];
        a->elem[j - 1] = a->elem[j] ^ a->elem[j - 1];
    }
    a->elem[idx] = val;
    a->cur++;
    return 0;  // success
}

int _remove(Seq* a, int idx) {
    if (idx < 0 || idx > a->cur) return -1;
    for (int j = idx; j < a->cur; j++) a->elem[j] = a->elem[j + 1];
    a->cur--;
    return 0;  // success
}

void _output(const Seq* a) {
    std::cout << "Array Values: " << std::endl;
    for (int j = 0; j <= a->cur; j++) std::cout << a->elem[j] << ' ';
    std::cout << std::endl;
}

void _clear(Seq* a) {
    a->n = 0;
    a->cur = -1;
    free(a->elem);
}

// Single List
//
typedef struct node {
    int elem;
    struct node* nxt;
} Node;

typedef struct slist {
    int n;
    Node* head;
} Slist;

void _init_slist(Slist* s_lst) {
    s_lst->n = 0;
    s_lst->head = nullptr;
}

int _find_slist(Slist* s_lst, const int& index) {
    if (!s_lst || !s_lst->head || index < 0 || index >= s_lst->n) return -1;
    int cur = 0;
    Node* ptr = s_lst->head;  // Damned Warning from Nowhere
    while (ptr->nxt && cur < index) {
        ptr = ptr->nxt;
        cur++;
    }
    return ptr ? ptr->elem : -1;
}

int _insert_slist(Slist* s_lst, const int& idx, const int& val) {
    if (!s_lst || idx < 0 || idx > s_lst->n) return -1;
    if (!s_lst->head) {
        if (idx != 0) {
            return -1;
        } else {
            s_lst->head = (Node*)malloc(sizeof(Node));
            s_lst->head->elem = val;
            s_lst->head->nxt = nullptr;
            s_lst->n++;
            return 0;
        }
    } else {
        int cur = 0;
        Node *ptr = s_lst->head, *dum = nullptr;
        while (ptr->nxt && cur < idx) {
            dum = ptr;
            ptr = ptr->nxt;
            cur++;
        }
        if (!dum) {
            dum = (Node*)malloc(sizeof(Node));
            dum->elem = val;
            dum->nxt = ptr;
            s_lst->n++;
            s_lst->head = dum;
        } else if (!ptr->nxt && idx == s_lst->n) {
            ptr->nxt = (Node*)malloc(sizeof(Node));
            ptr->nxt->elem = val;
            ptr->nxt->nxt = nullptr;
            s_lst->n++;
        } else {
            dum->nxt = (Node*)malloc(sizeof(Node));
            dum->nxt->elem = val;
            dum->nxt->nxt = ptr;
            s_lst->n++;
            return cur == idx ? 0 : -1;
        }
        return 0;
    }
}

int _remove_slist(Slist* s_lst, const int& idx) {
    if (idx < 0 || idx >= s_lst->n || !s_lst->head) return -1;
    Node *ptr = s_lst->head, *dum = nullptr;
    if (idx == 0) {
        s_lst->head = ptr->nxt ? ptr->nxt : nullptr;
        free(ptr);
        s_lst->n--;
    } else {
        int cur = 0;
        while (ptr->nxt && cur < idx) {
            dum = ptr;
            ptr = ptr->nxt;
            cur++;
        }
        if (cur != idx) return -1;
        dum->nxt = ptr->nxt;
        free(ptr);
        s_lst->n--;
    }
    return 0;
}

void _clear_slist(Slist* s_lst) {
    if (!s_lst || !s_lst->head) return;
    Node *ptr = s_lst->head, *dum = nullptr;
    if (!ptr->nxt) {
        free(ptr);
        s_lst->n = 0;
        s_lst->head = nullptr;
    } else {
        while (ptr->nxt) {
            dum = ptr;
            ptr = ptr->nxt;
            free(dum);
        }
        free(ptr);
        s_lst->n = 0;
        s_lst->head = nullptr;
    }
}

void _output_slist(Slist* s_lst) {
    std::cout << "Single List Values: " << std::endl;
    if (!s_lst || !s_lst->head) {
        std::cout << std::endl;
        return;
    }
    Node* ptr = s_lst->head;
    if (!ptr->nxt) {
        std::cout << ptr->elem << ' ' << std::endl;
    } else {
        while (ptr->nxt) {
            std::cout << ptr->elem << ' ';
            ptr = ptr->nxt;
        }
        std::cout << ptr->elem << ' ' << std::endl;
    }
}

// Invert List
//
void _invert_slist(Slist* s_lst) {
    if (!s_lst || !s_lst->head || !s_lst->head->nxt) return;
    Node *rig = s_lst->head, *mid = nullptr, *lef = nullptr;
    while (rig->nxt) {
        mid = rig;
        rig = rig->nxt;
        if (lef) {
            mid->nxt = lef;
            lef = mid;
        } else {
            mid->nxt = nullptr;
            lef = mid;
        }
    }
    rig->nxt = mid;
    s_lst->head = rig;
}

// Quick Sort
//
void _output_vec(std::vector<int> vec) {
    std::cout << "Vector Values: " << std::endl;
    for (auto val : vec) std::cout << val << ' ';
    std::cout << std::endl << std::endl;
}

void _qsort_vec(std::vector<int>& vec) {
    int n = vec.size();
    auto qsort = [&](auto& qsort, int lef, int rig) -> void {
        if (lef >= rig) return;
        int low = lef, high = rig;
        while (lef + 1 < rig) {
            while (lef < rig && vec[lef] < vec[rig]) lef++;
            std::swap(vec[lef], vec[rig]);
            while (lef < rig && vec[rig] > vec[lef]) rig--;
            std::swap(vec[lef], vec[rig]);
        }
        if (vec[lef] > vec[rig]) std::swap(vec[lef], vec[rig]);
        qsort(qsort, low, lef - 1);
        qsort(qsort, rig + 1, high);
    };
    qsort(qsort, 0, n - 1);
}

void _qsort_slist(Slist* s_lst) {
    if (!s_lst) return;
    std::vector<int> vec = {};
    Node* ptr = s_lst->head;
    while (ptr) {
        vec.push_back(ptr->elem);
        ptr = ptr->nxt;
    }
    _qsort_vec(vec);
    ptr = s_lst->head;
    for (auto val : vec) {
        if (!ptr) return;
        ptr->elem = val;
        ptr = ptr->nxt;
    }
}

// Polynomial
//
typedef struct pNode {
    int coef;
    int exp;
    struct pNode* nxt;
} PNode;

typedef struct polynomial {
    PNode* head;
} Polynomial;

void _qsort_exp(std::vector<std::vector<int>>& vals) {
    int n = vals.size();
    auto qsort = [&](auto& qsort, int lef, int rig) -> void {
        if (lef >= rig) return;
        int low = lef, high = rig;
        while (lef + 1 < rig) {
            while (lef < rig && vals[lef][1] < vals[rig][1]) {
                lef++;
            }
            std::swap(vals[lef], vals[rig]);
            while (lef < rig && vals[rig][1] > vals[lef][1]) {
                rig--;
            }
            std::swap(vals[lef], vals[rig]);
        }
        if (vals[lef][1] > vals[rig][1]) {
            std::swap(vals[lef], vals[rig]);
        }
        qsort(qsort, low, lef - 1);
        qsort(qsort, rig + 1, high);
    };
    qsort(qsort, 0, n - 1);
}

void _init_poly(Polynomial* poly, std::vector<std::vector<int>>& vals) {
    if (!poly || vals.empty()) return;
    _qsort_exp(vals);
    poly->head = (PNode*)malloc(sizeof(PNode));
    PNode *ptr = poly->head, *dum = nullptr;
    for (auto val : vals) {
        int &coef = val[0], &exp = val[1];
        ptr->coef = coef;
        ptr->exp = exp;
        ptr->nxt = (PNode*)malloc(sizeof(PNode));
        dum = ptr;
        ptr = ptr->nxt;
    }
    free(ptr);
    dum->nxt = nullptr;
}

void _output_poly(Polynomial* poly) {
    if (!poly) return;
    PNode* ptr = poly->head;
    std::cout << "Polynomial coefficients & exponents: " << std::endl;
    while (ptr) {
        std::cout << ptr->coef << "x^" << ptr->exp << " + ";
        ptr = ptr->nxt;
    }
    std::cout << "\b\b " << std::endl;
}

std::vector<std::vector<int>> poly2vec(Polynomial* poly) {
    if (!poly) return std::vector<std::vector<int>>();
    std::vector<std::vector<int>> vec = {};
    PNode* ptr = poly->head;
    while (ptr) {
        vec.push_back({ptr->coef, ptr->exp});
        ptr = ptr->nxt;
    }
    return vec;
}

Polynomial* sum_fxgx(Polynomial* poly1, Polynomial* poly2) {
    if (!poly1 || !poly2) return nullptr;
    std::vector<std::vector<int>> vec1 = poly2vec(poly1),
                                  vec2 = poly2vec(poly2);
    std::vector<std::vector<int>> vec = {};
    int i = 0, j = 0;
    while (i < vec1.size() || j < vec2.size()) {
        if (i == vec1.size()) {
            vec.push_back({vec2[j][0], vec2[i][1]});
            j++;
        } else if (j == vec2.size()) {
            vec.push_back({vec1[i][0], vec1[i][1]});
            i++;
        } else {
            if (vec1[i][1] == vec2[j][1]) {
                vec.push_back({vec1[i][0] + vec2[j][0], vec1[i][1]});
                i++;
                j++;
            } else if (vec1[i][1] < vec2[j][1])
                i++;
            else
                j++;
        }
    }
    Polynomial* sum = (Polynomial*)malloc(sizeof(Polynomial));
    sum->head = (PNode*)malloc(sizeof(PNode));
    PNode *ptr = sum->head, *dum = nullptr;
    for (auto val : vec) {
        if (val[0] == 0) continue;
        int &coef = val[0], &exp = val[1];
        ptr->coef = coef;
        ptr->exp = exp;
        ptr->nxt = (PNode*)malloc(sizeof(PNode));
        dum = ptr;
        ptr = ptr->nxt;
    }
    free(ptr);
    dum->nxt = nullptr;
    return sum;
}

Polynomial* prod_fxgx(Polynomial* poly1, Polynomial* poly2) {
    if (!poly1 || !poly2) return nullptr;
    std::vector<std::vector<int>> vec1 = poly2vec(poly1),
                                  vec2 = poly2vec(poly2);
    int min_exp = vec1[0][1] + vec2[0][1];
    int max_exp = vec1[vec1.size() - 1][1] + vec2[vec2.size() - 1][1];
    std::vector<std::vector<int>> vec(max_exp - min_exp + 1, {0, 0});
    for (int i = 0; i < vec1.size(); i++) {
        for (int j = 0; j < vec2.size(); j++) {
            vec[vec1[i][1] + vec2[j][1] - min_exp][0] +=
                vec1[i][0] * vec2[j][0];
            vec[vec1[i][1] + vec2[j][1] - min_exp][1] = vec1[i][1] + vec2[j][1];
        }
    }
    Polynomial* prod = (Polynomial*)malloc(sizeof(Polynomial));
    prod->head = (PNode*)malloc(sizeof(PNode));
    PNode *ptr = prod->head, *dum = nullptr;
    for (auto val : vec) {
        if (val[0] == 0) continue;
        int &coef = val[0], &exp = val[1];
        ptr->coef = coef;
        ptr->exp = exp;
        ptr->nxt = (PNode*)malloc(sizeof(PNode));
        dum = ptr;
        ptr = ptr->nxt;
    }
    free(ptr);
    dum->nxt = nullptr;
    return prod;
}

int main(void) {
    // Linear Array
    //
    Seq* a = (Seq*)malloc(sizeof(Seq));
    int n = 10, statu = 0, index;
    _init(a, n);
    statu += _insert(a, 0, 1);
    statu += _insert(a, 0, 2);
    statu += _insert(a, 0, 3);
    _output(a);
    index = _find(a, 2);
    std::cout << std::endl << "Find index of val 2: " << index << std::endl;
    statu += _remove(a, 1);
    _output(a);
    _clear(a);
    std::cout << std::endl << "Statu: " << statu << std::endl << std::endl;

    // List
    //
    Slist* s_lst = (Slist*)malloc(sizeof(Slist));
    _init_slist(s_lst);
    statu += _insert_slist(s_lst, 0, 2);
    statu += _insert_slist(s_lst, 0, 3);
    statu += _insert_slist(s_lst, 2, 1);
    statu += _insert_slist(s_lst, 2, 4);
    std::cout << "Single List Length: " << s_lst->n << std::endl;
    _output_slist(s_lst);
    index = _find_slist(s_lst, 2);
    std::cout << std::endl << "Find index of val 2: " << index << std::endl;
    statu += _remove_slist(s_lst, 1);
    _output_slist(s_lst);
    std::cout << std::endl << "Statu: " << statu << std::endl << std::endl;

    // Invert List
    //
    std::cout << "Invert Single List: " << std::endl;
    _invert_slist(s_lst);
    _output_slist(s_lst);
    std::cout << std::endl;
    // Quick Sort List
    _qsort_slist(s_lst);
    _output_slist(s_lst);
    std::cout << std::endl;
    // Clear List
    _clear_slist(s_lst);

    // Polynomial
    //
    std::vector<std::vector<int>> fx_vals = {{2, 4}, {2, 3}, {3, 1}, {6, 0}};
    std::vector<std::vector<int>> gx_vals = {{3, 3}, {1, 2}, {2, 1}, {4, 0}};

    Polynomial* fx = (Polynomial*)malloc(sizeof(Polynomial));
    _init_poly(fx, fx_vals);
    std::cout << "Polynomial f(x):" << std::endl;
    _output_poly(fx);

    std::cout << std::endl;

    Polynomial* gx = (Polynomial*)malloc(sizeof(Polynomial));
    _init_poly(gx, gx_vals);
    std::cout << "Polynomial g(x):" << std::endl;
    _output_poly(gx);

    Polynomial* sum = sum_fxgx(fx, gx);
    std::cout << std::endl << "Polynomial f(x) + g(x):" << std::endl;
    _output_poly(sum);

    Polynomial* prod = prod_fxgx(fx, gx);
    std::cout << std::endl << "Polynomial f(x) * g(x):" << std::endl;
    _output_poly(prod);

    return 0;
}
