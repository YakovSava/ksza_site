# include <string>
# include <fstream>
using namespace std;

struct stats {
	int home_moved;
	int pay_moved;
	int pays_and_moved;
}


void create_file(string file, string all_files) {
	ofstream file(file.c_str());
}