#include <iostream>
#include <string>
#include <vector>

int main(void) {
    std::vector<char> ans = {'L', 'A', 'N', 'Q', 'I', 'A', 'O'};
    int cur = 0;
    std::string txt = "";
    std::cin >> txt;

    int i = 0;
    while (txt[i] != '\0') {
        if (txt[i] == ans[cur]) cur++;
        i++;
    }
    if (cur == ans.size())
        std::cout << "YES";
    else
        std::cout << "NO";

    return 0;
}