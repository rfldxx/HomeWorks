#include "my_lib.h"

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
