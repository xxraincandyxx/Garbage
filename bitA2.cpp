#include <cstdlib>
#include <iostream>


void out_intarray(int* values, int length) {
	for (int idx = 0; idx < length; idx++) {
		std::cout << values[idx] << ' ';
	}
	std::cout << std::endl;
}


void out_floatarray(float* values, int length) {
	for (int idx = 0; idx < length; idx++) {
		std::cout << values[idx] << ' ';
	}
	std::cout << std::endl;
}


void _qsort(float* values, int* by, int left, int right) {
	if (left >= right) { return; }

	int lcursor = left;
	int rcursor = right;
	int threshold = values[lcursor];
	int thresholdby = by[lcursor];

	while (lcursor < rcursor) {
		while (values[rcursor] > threshold && lcursor < rcursor) { rcursor--; }
		values[lcursor] = values[rcursor];
		by[lcursor] = by[rcursor];
		while (values[lcursor] < threshold && lcursor < rcursor) { lcursor++; }
		values[rcursor] = values[lcursor];
		by[rcursor] = by[lcursor];
	}
	values[lcursor] = threshold;
	by[lcursor]  = thresholdby;

	_qsort(values, by, left, lcursor - 1);
	_qsort(values, by, lcursor + 1, right);
}


float rho_func(float vi, int ki, int wi) {
	return (vi - (float)(ki + 1)) / (float)wi;
}


float reverse_func(float rho, int wi, int ki) {
	return rho * wi + (float)ki;
}


void resort(float* rho, int* key, int cur) {
	float tmp = 0.;
	for (int i = cur; i >= 0; i--) {
		if (rho[i] > rho[cur]) {
			tmp = rho[i];
			rho[i] = rho[cur];
			rho[cur] = tmp;
			key[i] = key[cur] ^ key[i];
			key[cur] = key[i] ^ key[cur];
			key[i] = key[cur] ^ key[i];
		}
	}
}


float solution(int N, int W, int** table) {
	// table: [weight, value]
	float* rho = (float*)malloc(N * sizeof(float));     // (v_i-(k_i+1))/(w_i(k_i+1))
	int* key = (int*)malloc(N * sizeof(int));	    // key
	int* kache = (int*)malloc(N * sizeof(int));         // k_i
	int* wache = (int*)malloc(N * sizeof(int));         // w_i
	int* vache = (int*)malloc(N * sizeof(int));	    // v_i
	float* values = (float*)malloc(N * sizeof(float));  // values_i
	int i = 0;

	// init rho & kache: O(N)
	for (; i < N; i++) {
		key[i] = i;
		kache[i] = 0;
		values[i] = 0.;
		wache[i] = table[i][0];
		vache[i] = table[i][1];
		rho[i] = rho_func((float)table[i][1], 0, table[i][0]);  // given k_i = 0
		std::cout << rho[i] << std::endl;
	}
	std::cout << "$$$$" << std::endl << std::endl;
	free(table);

	// qsort: O(N*logN)
	_qsort(rho, key, 0, N - 1);

	int w = 0;
	int n = N - 1;
	float value = 0.;
	while (n >= 0) {
		if (w + wache[key[n]] <= W && rho[n] > 0.) {
			value = (float)(kache[key[n]] + 1.) * ((float)vache[key[n]] - (float)(kache[key[n]] + 1.));
			std::cout << "% " << value << " %" << std::endl;
			if (value > values[key[n]]) {
				values[key[n]] = value;
				value = 0.;
			} else {
				value = 0.;
				n--;
				continue;
			}
			w += wache[key[n]];
			kache[key[n]]++;
			rho[n] -= 1 / (float)wache[key[n]];
			resort(rho, key, n);
			out_floatarray(rho, n);
			std::cout << "#####" << std::endl;
		} else { n--; }  // deprecated the last elem
		// std::cout << N << std::endl;
	}

	float v = 0.;
	for (i = 0; i < N; i++) { v += values[i]; }

	free(kache);
	free(wache);
	free(vache);
	free(values);
	return v;
}


int main(void) {
	int N = 0;
	int W = 0;
	scanf("%d %d", &N, &W);
	
	int** table = (int**)malloc(N * sizeof(int*));
	for (int i = 0; i < N; i++) {
		table[i] = (int*)malloc(2 * sizeof(int));
		scanf("%d %d", &table[i][0], &table[i][1]);
	}
	
	float v = solution(N, W, table);
	free(table);
	std::cout << std::endl << v << std::endl;
	return 0;
}

