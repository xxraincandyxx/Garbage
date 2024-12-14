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

#include <iostream>
#include <graph.hpp>
/*
    Declaration:
        1. the class initialization must in source file initialize, not in header file
        2. The header file (.hpp or .h) is generally meant for declarations, while the source file contains the actual implementations.
*/
Graph::Graph(int number_v) {
    this->n = number_v;
    this->n_edges = 0;
    adjacency = new Node* [n]; // allocate memory for adjacency list
    
    // initialize each adjacency list to nullptr
    for (int i = 0; i < n; i++) {
        adjacency[i] = nullptr;
    }
}

// destructor to free dynamically allocated memory
void Graph(){
    for(int i = 0; i < n; i++){
        Node* head = adjacency[i];
        while(head != nullptr){
            Node* temp = head;
            head = head->nextArc;
            delete temp;
        }
    }
    delete[] adjacency;
}

// get the number of edges
int Graph::get_edge_count() const {
    return n_edges;
}

// get the number of vertices
int Graph::get_vertex_count() const {
    return n;
}

void Graph::add_edge(int vertex1, int vertex2, int weight){
    Node* edge1 = new Node{vertex2, weight, this->adjacency[vertex1]};
    this->adjacency[vertex1] = edge1;

    Node* edge2 = new Node{vertex1, weight, this->adjacency[vertex2]};
    this->adjacency[vertex2] = edge2;

    this->n_edges += 1;
}

void Graph::print_graph() const{
    for(int i = 0; i < this->n; i++) {
            cout << i << ": ";
            Node* head = this->adjacency[i];
            while (head != nullptr) {
                cout << "(" << head->adjVex << ", " << head->w << "), ";
                head = head->nextArc;
            }
            cout << endl;
    }
}

void Graph::del_edge(int vertex1, int vertex2){
    if (vertex1 < 0 || vertex2 < 0 || vertex1 > n - 1 || vertex2 > n - 1 || vertex1 == vertex2) { return; }
    Node* curr_vertex = adjacency[vertex1];
    Node* prev_vertex = nullptr;

    while(curr_vertex != nullptr && curr_vertex->adjVex != vertex2) {
        prev_vertex = curr_vertex;
        curr_vertex = curr_vertex->nextArc;
    }

    if (curr_vertex != nullptr) {
        if (prev_vertex == nullptr) {
            adjacency[vertex1] = curr_vertex->nextArc;
        } else {
            prev_vertex->nextArc = curr_vertex->nextArc;
        }
        delete curr_vertex;
        n_edges -= 1;
    }

    curr_vertex = adjacency[vertex2];
    prev_vertex = nullptr;

    while (curr_vertex != nullptr && curr_vertex->adjVex != vertex1){
        prev_vertex = curr_vertex;
        curr_vertex = curr_vertex->nextArc;
    }

    if (curr_vertex != nullptr){
        if (prev_vertex == nullptr) {
            adjacency[vertex2] = curr_vertex->nextArc;
        } else {
            prev_vertex->nextArc = curr_vertex->nextArc;
        }
        delete curr_vertex;
    }
}

void Graph::dfs_utils(int vertex, vector<bool>& visited) const{
    cout << " -> " << vertex;
    visited[vertex] = true;

    Node* curr_vertex = adjacency[vertex];
    while(curr_vertex != nullptr){
        int next_vertex = curr_vertex->adjVex;
        if(visited[next_vertex] == false){
            dfs_utils(next_vertex, visited);
        }
        curr_vertex = curr_vertex->nextArc;
    }
    return;
}

void Graph::dfs(int start_vertex) const{
    vector<bool> visited(n, false);
    dfs_utils(start_vertex, visited);
    return;
}

void breath_first_search(int start_vertex, vector<bool>& visited) {
    visited[start_vertex] = true;
    queue<int> queue;
    queue.push(start_vertex);
    while(!queue.empty()){
        int vertex = queue.front();
        queue.pop();
        cout << " -> " << vertex;
        Node* curr_vertex = adjacency[vertex];
        while(curr_vertex != nullptr){
            int next_vertex = curr_vertex->adjVex;
            if(visited[next_vertex] == false){
                visited[next_vertex] = true;
                queue.push(next_vertex);
            }
            curr_vertex = curr_vertex->nextArc;
        }
    }
    return;
}

void algofoo (int start_vertex) const{
    priority_queue<pair<int, int>, vector<pair<int, int>>, Compare> open;
    vector<bool> visited(n, false);
    open.push({0, start_vertex});
    int total_weight = 0;
    while (!open.empty()){
        auto [curr_weight, curr_vertex] = open.top();
        open.pop();
        if (visited[curr_vertex]) continue;
        visited[curr_vertex] = true;
        total_weight += curr_weight;
        Node* adj = adjacency[curr_vertex];
        while (adj != nullptr) {
            if (visited[adj->adjVex] == false) {
                open.push({adj->w, adj->adjVex});
            }
            adj = adj->nextArc;
        }
    }
}
