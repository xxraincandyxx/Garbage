#include <iostream>
#include <cstdio>


void output_array(int*, int);
int cmp(const void*, const void*);


int cmp(const void* a, const void* b) {
	return ( *(int*)a - *(int*)b );
}


double minimumAverage(int* nums, int numsSize) {
	int times = (int)(numsSize / 2);
	qsort(nums, numsSize, sizeof(int), cmp);

	int left = 0;
	int right = numsSize - 1;

	float res = (float)nums[right];
	float ave = 0.;
	for (int t = 0; t < times; t++) {
		ave = (float)(nums[right] + nums[left]) / 2;
		if (ave < res) { res = ave; }
		
		left++;
		right--;
	}
	
	return res;
}


void output_array(int* nums, int numsSize) {
	for (int idx = 0; idx < numsSize; idx++) {
		printf("%d ", nums[idx]);
	}
	return;
}
