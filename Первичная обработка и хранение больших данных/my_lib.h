#include <bits/stdc++.h>
using namespace std;

// ======================================================================================================
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
// ....updated_get....


// ======================================================================================================
// Quantiles
// медиана отсортированного подмассива [l, r]
double median(const vector<double>& xx, int l, int r) {
    int n = r-l+1;
    // нечётное количество
    if( n%2 ) return xx[l + n/2];
    return (xx[l + n/2 - 1] + xx[l + n/2])/2;
}

// квартили
tuple<double, double, double> quntiels(vector<double> xx) {
    int n = xx.size();
    sort( xx.begin(), xx.end() );

    // не включая элементы которые использовались для нахождения медианы
    int lm = (n-1)/2 - 1;
    int rm =    n /2 + 1;
    return { median(xx, 0, lm),  median(xx, 0, n-1), median(xx, rm, n-1) };
}


// ======================================================================================================
// Normalizing
// auto f - функция нормировки одного элемента: f(x, x_min, x_max)
vector<double> norm(vector<double> data, auto f) {
    double mn = data[0], mx = data[0];
    for(auto e : data) {
        mn = min(mn, e);
        mx = max(mx, e);
    }

    vector<double> result(data.size());
    for(int i = 0; auto e : data)
        result[i++] = f(e, mn, mx);
    return result;
}

double lin_norm(double x, double mn, double mx) { return (x-mn) / (mx-mn); }
double exp_norm(double x, double mn, double mx) { return 1 - expl(1 - x/mn); }

