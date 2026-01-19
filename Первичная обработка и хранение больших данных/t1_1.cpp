#include <bits/stdc++.h>
using namespace std;

// ....updated_get....
#define For(i, n) for(int i = 0; i < n; i++)

string totime(int t) {
    return to_string(t/3600) + ':' + to_string((t/60)%60) + ':' + to_string(t%60);
}

int updated_get_int(const auto& s, int& i) {
    int r = 0;
    while( '0' <= s[i] && s[i] <= '9' ) {
        r = 10*r + (s[i] - '0');
        i++;
    }
    i++;  // пропуск разделителя 
    return r;
}

int updated_get_time(const auto& s, int& i, int hms = 3) {
    int r = 0;
    For(_, hms) {  // часы, минуты, секуды
        r = 60*r + updated_get_int(s, i);
    }
    return r; //%3600; // без часов
}

int updated_get_date(const auto& s, int& i) {
    int d = updated_get_int(s, i);
    int m = updated_get_int(s, i);
    int y = updated_get_int(s, i);

    return 100*m + d; // без года
}
// ....updated_get....

string updated_get_string(const auto& s, int& i, char delim) {
    string result;
    while( s[i] != delim ) {
        if( s[i]  ) result += s[i];
        i++;
    }
    i++;  // пропуск разделителя 
    return result;
}

double updated_get_double(const auto& s, int& i) {
    double result = updated_get_int(s, i);

    //  s[i-1] - так как в updated_get_int всегда есть пропуск разделителя 
    if( s[i-1] == '.' ) {  // есть дробная часть
        int j = i;
        int rem = updated_get_int(s, i);
        
        double pow10 = 1;
        for(int k = 1; k < i-j; k++) pow10 *= 10;

        result += rem / pow10;
    }

    return result;
}

// из-за форма windows - он в конце строки добавляет какой-то непонятный char
// !!! вообще лучше было бы если в конце каждой строчке был delim, а не только '\n'
#define need_del_last 1


vector<string> get() {
    char delim = ',';

    string s;
    if( !getline(cin , s) ) return {};
    if(need_del_last) s.pop_back();
    s += delim;

    cout << "READ: " << s << endl;

    vector<string> r;
    int indx = 0;
    For(_, 2) r.push_back( updated_get_string(s, indx, delim) );
    return r;
}


int main() {
    setlocale(LC_ALL, "Russian");

    string search;
    getline(cin , search);
    if(need_del_last) search.pop_back();

    vector<string> result;
    while(1) { // предназначенно для считывания из файла - пока есть данные
        auto line = get();
        if( !line.size() ) break;

        if( line[1] == search)
            result.push_back( line[0] );
    }

    cout << result.size() << endl;
    for(auto e : result) cout << e << endl;
}
