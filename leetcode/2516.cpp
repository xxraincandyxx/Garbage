#include <iostream>


using namespace std;


int main(void) {
	int slen = 12;
 	char s[] = { 'a', 'a', 'b', 'a', 'a', 'a', 'a', 'c', 'a', 'a', 'b', 'c' };
	int k = 1;
	int hash_map[3] = { 0 };
	int left_cursor = 0, right_cursor = slen - 1;
	int left_buffer = 0, right_buffer = 0;
	int out_check = 0;
	int left_tmp = 0;
	int right_tmp = 0;

	do {
		left_tmp = (int)(s[left_cursor] - 'a');
		hash_map[left_tmp]++;
		if (hash_map[left_tmp] == k) {
			left_buffer = left_cursor + 1;
			out_check++;	
		}

		right_tmp = (int)(s[right_cursor] - 'a');
		hash_map[right_tmp]++;
		if (hash_map[right_tmp] == k) {
			right_buffer = slen - right_cursor;
			out_check++;
		}
		
		if (out_check == 3) {
			cout << left_buffer + right_buffer << endl;
			return 0;
		}
		
		left_cursor++;
		right_cursor--;
			
} while (left_cursor <= right_cursor);

	cout << "-1" << endl; 
	return -1;	
}