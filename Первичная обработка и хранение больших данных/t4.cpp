#include "my_lib.cpp"

// из-за форма windows - он в конце строки добавляет какой-то непонятный char
// !!! вообще лучше было бы если в конце каждой строчке был delim, а не только '\n'
#define need_del_last 1


// id,NAME,WIDTH,PRICE,POWER,GRASS,AREA,DESCRIPTION

tuple<int, vector<double>, int> get() {  // return id,WIDTH,PRICE,POWER,GRASS,AREA,TYPE
    char delim = ',';

    string s;
    if( !getline(cin , s) ) return {};
    if(need_del_last) s.pop_back();
    s += delim;

    // cout << "READ: " << s << endl;

    int indx = 0;
    int id = updated_get_int(s, indx);

    updated_get_string(s, indx, delim);

    vector<double> spec;
    For(_, 5) {
        spec.push_back( updated_get_double(s, indx) );
    }

    string description = updated_get_string(s, indx, delim);
    
    // всё ок с параметром "Ширина скашиваемой полосы"
    if( spec[0] ) return {id, spec, 0};



    // нет параметра "Ширина скашиваемой полосы"
    int type = 0;
    
    // Если в описании газонокосилки встречались слова "узкая|узкие|узкую|узкой", то значение восстанавливалось как медиана по существующим в исходном датасете значениям в диапазоне от $30$ до $35$.
    if( !type ) {
        bool ok = 0;
        // Тихий ужас с этими раскладками.....
        for(auto pattern : {"узкая" , "узкие", "узкую" , "узкой", "Узкая" , "Узкие", "Узкую" , "Узкой"})
            ok |= description.find(pattern) != string::npos;

        if(ok) type = 1;
    }

    // - Если встречались слова "средняя ширина"/"ширина средняя", то значение восстанавливалось как округленное до целого среднее арифметическое по существующим значениям в диапазоне от $36$ до $40$.
    if( !type ) {
        bool ok = 0;
        for(auto pattern : {"средняя ширина", "ширина средняя", "Средняя ширина", "Ширина средняя"})
            ok |= description.find(pattern) != string::npos;

        if(ok) type = 2;
    }

    // - Если встречались слова ("широкая" и "полоса")/("широкие" и "полосы"), то значение восстанавливалось как медиана по существующим значениям в диапазоне от $41$ до $45$.
    if( !type ) {
        // захаркодим
        bool ok = 0;
        ok |= (description.find("широкая") != string::npos) && (description.find("полоса") != string::npos);
        ok |= (description.find("широкие") != string::npos) && (description.find("полосы") != string::npos);

        ok |= (description.find("Широкая") != string::npos) && (description.find("полоса") != string::npos);
        ok |= (description.find("Широкие") != string::npos) && (description.find("полосы") != string::npos);
        
        ok |= (description.find("широкая") != string::npos) && (description.find("Полоса") != string::npos);
        ok |= (description.find("широкие") != string::npos) && (description.find("Полосы") != string::npos);

        ok |= (description.find("Широкая") != string::npos) && (description.find("Полоса") != string::npos);
        ok |= (description.find("Широкие") != string::npos) && (description.find("Полосы") != string::npos);

        if(ok) type = 3;
    }

    cout << type << " : " << description << endl;

    return {id, spec, type};
}




int main() {
    setlocale(LC_ALL, "Russian");

    vector<tuple<int, vector<double>, int>> Table;
    while(1) { // предназначенно для считывания из файла - пока есть данные
        auto tt = get();
        if( !get<1>(tt).size() ) break;

        Table.push_back(tt);
    }

    int N = Table.size();
    cout << "N = " << N << endl;


    cout << endl;
    // ======================================================================================================
    // 1.1. По существующим в исходном датасете значениям:
    //          sum1 - от $30$ до $35$. - ищем медиану
    //          sum2 - от $36$ до $40$. - округленное до целого среднее арифметическое
    //          sum3 - от $41$ до $55$. - ищем медиану
    vector<double> xx1, xx3;
    double sum2 = 0;
    int n2 = 0;
    for(auto [id, spec, type] : Table) {
        double x = spec[0];
        if( 30 <= x && x <= 35 ) { xx1.push_back(x); }
        if( 36 <= x && x <= 40 ) { sum2 += x; n2++; }
        if( 41 <= x && x <= 55 ) { xx3.push_back(x); }
    }


    double x1 = get<1>(quntiels(xx1)), x3 = get<1>(quntiels(xx3));
    double x2 = (int)(sum2/n2);
    if( (sum2/n2) - x2 >= 0.5 ) x2 += 1;

    cout << "Median WIDTH (by WIDTH in [30, 35]):  " << x1 << " (cnt=" << xx1.size() << ")\n";
    cout << "Avg    WIDTH (by WIDTH in [36, 40]):  " << (sum2/n2) << " -> " << x2 << endl;
    cout << "Median WIDTH (by WIDTH in [41, 55]):  " << x3 << " (cnt=" << xx3.size() << ")\n";

    
    // 1.2. Введите среднее арифметическое для параметра "Ширина скашиваемой полосы" после восстановления пропущенных значений:
    double sum = 0;
    for(auto& [id, spec, type] : Table) {
        // востанавливаем, в случае чего
        if( type == 1 ) spec[0] = x1;
        if( type == 2 ) spec[0] = x2;
        if( type == 3 ) spec[0] = x3;

        sum += spec[0];
    }
    cout << "Avg WIDTH after restoring values: " << sum/N << endl;



    cout << endl;
    // ======================================================================================================
    // 2. и 3.  
    //      2. Цены на газонокосилки имели очень большой разброс, и Юрий решил избавиться от вариантов, стоимость которых попадала под определение "экстремальных выбросов".
    //      3. Затем Юрий исключил записи, в которых все еще оставались пропущенные значения.
    vector<double> prices;
    for(auto [id, spec, type] : Table) {
        if( spec[1] == 0 ) continue;  // пропущенное значение

        prices.push_back(spec[1]);
    }

    auto [Q1, Q2, Q3] = quntiels(prices);

    sort(prices.begin(), prices.end());
    cout << "All PRICE (sorted): ";
    for(auto e : prices) cout << e <<  " "; cout << endl;

    cout << "Q1 = " << Q1 << ", Q2 = " << Q2 << ", Q3 = "  << Q3 << endl;

    double QL = Q1 - 3*(Q3-Q1), QR = QR = Q3 + 3*(Q3-Q1);
    cout << "PRICE is outlier if: " << "PRICE <= " << QL << " or "  << QR << " <= PRICE " << endl;


    // создаем новую таблицу без пропусков:
    vector<tuple<int, vector<double>>> clearTable;
    for(auto [id, spec, type] : Table) {
        bool skip = 0;
        // отсутствие значения
        for(auto e : spec) skip |= (e == 0);

        // выброс по цене
        skip |= (spec[1] <= QL) || (QR <= spec[1]);

        if( skip ) continue;

        // всё ок
        clearTable.push_back( {id, spec} );
    }

    // Введите количество оставшихся к рассмотрению газонокосилок:
    int L = clearTable.size();
    cout << "Remain after cleaning data: " << L << " elements" << endl;
 
    // Введите среднее арифметическое для параметра "Стоимость" полученного после обработки набора данных:
    sum = 0;
    for(auto [id, spec] : clearTable) sum += spec[1];
    cout << "Avg WIDTH after restoring values: " << sum/L << endl;


    
    cout << endl;
    // ======================================================================================================
    // 4. Параметры газонокосилок имеют разную размерность, так что Юрий решил экспоненциально нормировать значения числовых параметров.
    for(int t = 0; t < 5; t++) {
        vector<double> curr_param(L);
        for(int i = 0; i < L; i++) curr_param[i] = get<1>(clearTable[i])[t];

        auto norm_param = norm(curr_param, exp_norm);

        for(int i = 0; i < L; i++) get<1>(clearTable[i])[t] = norm_param[i];
    }

    // Введите нормированные значения параметров газнокосилки Gardez IER578 (её id == 57):
    for(int i = 0; i < L; i++) {
        if( get<0>(clearTable[i]) != 57 ) continue;

        cout << "Lawnmower (Gardez IER578 with id==57): ";
        cout << get<0>(clearTable[i]) << " ";
        for(auto e : get<1>(clearTable[i])) cout << e << " ";
        cout << endl;
    }



    cout << endl;
    // ======================================================================================================
    // 5. И наконец, Юрий составил целевую функцию, на основе которой определил 3 наиболее подходящие (на его взгляд) газонокосилки. При определении целевой функции он использовал следующие слагаемые:
    //      - Нормированная ширина скашиваемой полосы с коэффициентом 5
    //      - Стоимость как слагаемое вида (1 - нормированная стоимость) с коэффициентом 5
    //      - Нормированную мощность с коэффициентом 5
    //      - Нормированный объём травосборника с коэффициентом 5
    //      - Нормированную площадь скашиваемой поверхности с коэффициентом 2
    // Какие 3 газонокосилки являются лучшими (по целевой функции Юрия)? Введите три названия газонокосилок через запятую, например Cooper XWZ182, Nakita 74FHSC, Cooper INH176
    map<double, vector<int>> miku;
    
    for(auto& [id, spec] : clearTable) {
        // cost = 5*norm(WIDTH) + 5*(1 - norm(PRICE)) + 5*norm(POWER) + 5*norm(GRASS) + 2*norm(AREA)
        double cost = 5 * (spec[0] + 1-spec[1] + spec[2] + spec[3]) + 2*spec[4];
        miku[cost].push_back(id);
    }

    for(int h = 3; auto [cost, vv] : miku) {
        cout << "Loss = " << cost << " : on indx: ";
        for(auto i : vv) cout << i << " ";
        cout << endl;

        if( --h == 0 ) break;
    }
}
