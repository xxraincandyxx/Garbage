#include <iostream>
#include <cstdint>

int64_t dfs(int, int, int*);
int min_value(int, int);
int numberOfPermutations(int, int**, int, int*);

int main() {
	int** requirements = (int**)malloc(4 * sizeof(int*));
	for (int r = 0; r < 4; r++) {
		*(requirements + r) = (int*)malloc(2 * sizeof(int));
	}

	requirements[0][0] = 4;
	requirements[0][1] = 5;
	requirements[1][0] = 6;
	requirements[1][1] = 10;
	requirements[2][0] = 14;
	requirements[2][1] = 53;
	requirements[3][0] = 0;
	requirements[3][1] = 0;

	int* col = NULL;
	printf("%d", numberOfPermutations(15, requirements, 4, col));
	return 0;
}

int numberOfPermutations(int n, int** requirements, int requirementsSize, int* requirementsColSize) {
	int64_t MOD = 1000000007;
	int* req = (int*)malloc(n * sizeof(int));

	for (int i = 0; i < n; i++) { req[i] = -1; }
	req[0] = 0;
	for (int i = 0; i < requirementsSize; i++) {
		req[requirements[i][0]] = requirements[i][1];
	}

	if (req[0] > 0) { return 0; }
	
	int64_t ret = dfs(n - 1, req[n-1], req) % MOD;
    free(req);
    return ret;
}

int64_t dfs(int nperm, int ninv, int* req) {
	if (nperm == 0) { return 1; }
