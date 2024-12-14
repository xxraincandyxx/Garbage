#include <iostream>


void output_array(int* values, int length);
void quick_sort(int* values, int length, int left, int right);

int main() {
	int array[] = { 2, 0, 0, 4, 0, 9, 1, 0, 2, 2, 1, 2 };
	int length = 12;
	output_array(array, length);
	quick_sort(array, length, 0, length - 1);
	output_array(array, length);
	return 0;
}


void output_array(int* values, int length) {
	for (int idx = 0; idx < length; idx++) {
		printf("%d ", values[idx]);
	}
	putchar('\n');
	return;
}


void quick_sort(int* values, int length, int left, int right) {
    if (left >= right) { return; }
	
	int lcursor = left;
	int rcursor = right;
	
	int threshold = values[rcursor];
	while (lcursor < rcursor) {
		while (values[lcursor] <= threshold && lcursor < rcursor) { lcursor++; }
		values[rcursor] = values[lcursor];
		while (values[rcursor] >= threshold && lcursor < rcursor) { rcursor--; }
		values[lcursor] = values[rcursor];
	}
	values[rcursor] = threshold;

	quick_sort(values, length, left, rcursor - 1);
	quick_sort(values, length, rcursor + 1, right);
	return;
}