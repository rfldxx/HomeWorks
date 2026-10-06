#include <bits/stdc++.h>

using namespace std;


// создаём order_id

int random_SEED = 1;
// генератор имени
string murmuring(int n) {
    vector<string> syllables = {"ва","ви","гу","да","ди","ка","ла","ли","ма","ми","на","ни","ра","ре","ри", "ня", "сен", "ко"};
    string result;
    while( n-- ) result += syllables[rand()%syllables.size()];
    return result;
}

string translit(string s) {
    map<char, string> letter_translit = {
        {'а',  "a"}, {'б',   "b"}, {'в',  "v"}, {'г',  "g"}, {'д',  "d"},
        {'е',  "e"}, {'ё',  "yo"}, {'ж', "zh"}, {'з',  "z"}, {'и',  "i"},
        {'й',  "y"}, {'к',   "k"}, {'л',  "l"}, {'м',  "m"}, {'н',  "n"},
        {'о',  "o"}, {'п',   "p"}, {'р',  "r"}, {'с',  "s"}, {'т',  "t"},
        {'у',  "u"}, {'ф',   "f"}, {'х', "kh"}, {'ц', "ts"}, {'ч', "ch"},
        {'ш', "sh"}, {'щ', "sch"}, {'ъ',   ""}, {'ы',  "y"}, {'ь',   ""},
        {'э',  "e"}, {'ю',  "yu"}, {'я', "ya"},
    };
    string result;
    for(auto e : s) result += letter_translit[e];
    return result;
}

string generate_person() {
    string name = murmuring( 2 + (rand()%3) );

    // Первый email появился в 1971 году
    vector<string> email_domens = {"@gmail.com", "@abc.edu", "@mail.ru", "@corp.xd"};
    string email = translit(name) + to_string( 1971 + (rand()%(2026-1971+1)) ) + email_domens[rand()%email_domens.size()];

    char    phone[19];
    sprintf(phone, "+7(%03d)%03d-%02d-%02d", rand()%999, rand()%999, rand()%99, rand()%99);
  
    vector<string> surnames    = {"Уильямс", "Браун", "Стетхем", "Иванов", "Петров", "Попов", "Кузнецов", "Романов"};
    vector<string> patronymics = {"Михайлович", "Николаевич", "Павлович", "Александрович", "Святославович", "Мефодиевич", "Осипович", "Джонсон", "Стивенсон", "Робинсон"};
    name += " " + surnames[rand()%surnames.size()] + " " + patronymics[rand()%patronymics.size()];

    return "'" + name + "', '" + email + "', '" + phone + "'";
}


vector<tuple<string, int>> PRODUCTS = {
    {"Холодильник",                        20'000}, 
    {"Микроволновая печь",                 15'000},
    {"Духовой шкаф",                       30'000},
    {"Посудомоечная машина",               25'000},
    {"Варочная панель",                    40'000},
    {"Кофемашина",                         17'000},
    {"Кухонный комбайн",                   21'000},
    {"Электрический культиватор",          10'000},
    {"Электрическая газонокосилка",        13'000},
    {"Стиральная машина",                  33'333},
    {"Компьютер",                         111'111},
    {"Электронная вычислительная машина", 999'999},
    {"Нетбук",                            150'000},
    {"Ноутбук",                           150'000}
};

string generate_cart(int n) {
    string names, prices, quantities;
    int total = 0;

    while( n-- ) {
        auto [name, price] = PRODUCTS[rand()%PRODUCTS.size()];
        int cnt = rand()%5;  // может быть ноль товаров)
        
        names      += name             + (n ? ", " : "");
        prices     += to_string(price) + (n ? ", " : "");
        quantities += to_string(cnt)   + (n ? ", " : "");

        total += cnt*price;
    }

    return "'" + names + "', '" + prices + "', '" + quantities + "', " + to_string(total);
}

// "city " + ADRESSES[i] + " street"
vector<string> ADRESSES = {
    "Санкт-Петербург, А", "Спб, А", "Санкт-Петербург, В", "Спб, В",
    "Москва, А", "Мск, А", "Москва, Б", "Мск, Б",
    "Самовывоз"
};

vector<vector<string>> SUPPLY_CHAINS = {
    {"booked"},
    {"booked", "cancelled"},
    {"booked",    "paided"},
    {"booked",    "paided", "cancelled"},
    {"booked",    "paided", "completed"},
    {"booked",    "paided",   "shipped"},
    {"booked",    "paided",   "shipped", "cancelled"},
    {"booked",    "paided",   "shipped", "completed"},
    {             "paided"},
    {             "paided", "cancelled"},
    {             "paided", "completed"},
    {             "paided",   "shipped"},
    {             "paided",   "shipped", "cancelled"},
    {             "paided",   "shipped", "completed"},

};


int main() {
    srand      (random_SEED);
    mt19937 gen(random_SEED);
    vector<string> rows;

    int TOTAL_PERSONS = 500;

    int sum_of_repeats = 0, max_repeats = 0;  //для сбора Avg. и Max. (для интереса)
    int cnt_items = 0, cnt_items_with_repeats = 0;
    vector<int> supply_chain_size;
    for(int iteration = 0; iteration < TOTAL_PERSONS; iteration++) {
        string person = generate_person();
        
        int    repeats = __builtin_clz(rand() | 1);  // типо экспоненциальное распределение повторных покупок (в конце добавленно " | 1", т.к. у __builtin_clz аргемент должен быть ненулевым)
        sum_of_repeats += repeats;
        max_repeats = max(max_repeats, repeats);
        while( repeats-- ) {
            int cart_size = 1 + (rand()%PRODUCTS.size())/2;
            cnt_items += cart_size;
            string same_part = person + ", 'city " + ADRESSES[rand()%ADRESSES.size()] + " street', " + generate_cart(cart_size);
            
            int day = rand()%(26*360);
            auto& supply_chain = SUPPLY_CHAINS[rand()%SUPPLY_CHAINS.size()];
            supply_chain_size.push_back(supply_chain.size());
            for(auto status : supply_chain) {
                cnt_items_with_repeats += cart_size;
                rows.push_back("DATE '2020-01-01' + " + to_string(day) + ", " +  same_part + ", '" + status + "'");
                day += rand()%30;
            }
        }
    }
    cerr << "Avg. repeats of buying per person: " << 1.*sum_of_repeats/TOTAL_PERSONS << endl;
    cerr << "Max. repeats of buying for person: " << max_repeats << endl;
    cerr << "Total number of selected items in carts: " << cnt_items << " (with repeats: " << cnt_items_with_repeats << ")" << endl;


    // создаём "случайный" порядок order_id
    vector<int> used_id( supply_chain_size.size() );
    for(int i = rand()%100; auto& id : used_id) {
        id = i;
        i += 1 + (rand()%3);
    }
    std::shuffle(used_id.begin(), used_id.end(), gen);

    // раздаём order_id, так чтобы все записи из одной supply_chain имели одинаковый order_id
    for(int i = 0, k = 0; k < used_id.size(); k++) {
        for(int _ = 0; _ < supply_chain_size[k]; _++, i++) {
            rows[i] = to_string(used_id[k]) + ", " + rows[i];
        }
    }


    std::shuffle(rows.begin(), rows.end(), gen);


    cout << "DROP TABLE IF EXISTS orders_raw CASCADE;\n"
            "\n"
            "CREATE TABLE orders_raw (\n"
            "   order_id           INTEGER,\n"
            "   order_date         DATE,\n"
            "   customer_name      TEXT,          -- \"Иванов Иван Иванович\"\n"
            "   customer_email     TEXT,\n"
            "   customer_phone     TEXT,\n"
            "   delivery_address   TEXT,\n"
            "   product_names      TEXT,          -- \"Ноутбук, Мышь, Коврик\"\n"
            "   product_prices     TEXT,          -- \"85000, 1500, 500\"\n"
            "   product_quantities TEXT,          -- \"1, 1, 2\"\n"
            "   total_amount       INTEGER,\n"
            "   status             TEXT           -- \"delivered\"\n"
            ");\n\n";

    cout << "INSERT INTO orders_raw VALUES" << endl;
    for(int i = 0; i < rows.size(); i++) {
        cout << "\t(" << rows[i] << ")" << ",;"[i+1 == rows.size()] << endl;
    }
}

