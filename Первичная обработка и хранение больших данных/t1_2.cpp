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

// захардкожено!
pair<string, double> get() {
    char delim = ',';

    string s;
    if( !getline(cin , s) ) return {};
    if(need_del_last) s.pop_back();
    s += delim;

    // cout << "READ: " << s << endl;

    int indx = 0;
    string name = updated_get_string(s, indx, delim);

    double in2009 = 0, other_year;
    For(_, 13) {
        (_ == 11 ? in2009 : other_year) = updated_get_double(s, indx);
    }
    
    return {name, in2009};
}


int main() {
    setlocale(LC_ALL, "Russian");

    // нужные субъекты
    int n = 0;
    {   // трешш
        string s;
        getline(cin , s);
        if(need_del_last) s.pop_back();
        s += ',';
        int indx = 0;
        n = updated_get_int(s, indx);
    }

    set<string> need;
    for(int i = 0; i < n; i++) {
        string s;
        getline(cin , s);
        if(need_del_last) s.pop_back();
        s += ',';
        int indx = 0;
        need.insert( updated_get_string(s, indx, ',') );
    }
    

    cout << "SEARCH:\n";
    for(auto e : need) cout << e << endl;
    cout << endl;
    

    double sum = 0;
    while(1) { // предназначенно для считывания из файла - пока есть данные
        auto [name, in2009] = get();
        if( !name.size() ) break;

        if( !need.count(name) ) continue;
        
        cout << "[FIND] " << name << " : " << in2009 << endl;
        sum += in2009;
    }

    cout << "\nSUM: " << fixed << sum << endl;
}
    cout << fixed << sum << endl;
}
