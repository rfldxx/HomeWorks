#include "my_lib.h"

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
