#include <iostream>
using namespace std;
int main () {
    long long int length;
    string ainput;
    string binput;
    cin >> length;
    cin >> ainput;
    cin >> binput;
    int charcounter = 0;
    char x;
    int counter;
    int arr[length-1];
    for (char y : ainput, binput) {
        x  = int(y);
        arr[charcounter] = x;
        charcounter += 1;
    }

    for (int i = 0; i <= length; i++) {
        for (int j = i+2; j <= length; j++) {
            int sum = 0;
            for (int k = 0; k <= j; k++) {
            sum += arr[k];
            } 
            if ((sum - 48)/47 == 0) {
                counter += 1;
            }
            else if ((sum - 47)/48 == 0) {
                counter += 1;
            }
            else {
                counter += 0;
            }
        }
    }
    cout << counter;
}