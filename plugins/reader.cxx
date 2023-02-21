# include <fstream>
# include <string>
using namespace std;

class Reader {
	public:
		Reader(char* filename) {
			this->file.open(filename);
		}

		~Reader() {
			if (this->file.is_open()) {
				this->file.close();
			}
		}

		string readfile() {
			if (this->file.is_open()) {
				while (file >> line) {
					lines = this->concatinate(lines, line);
				}
			} else {
				this->lines = "bad open";
			}
			return this->lines;
		}
		
		void clear() {
			this->file.close();
		}

	private:
		string line, lines = "";
		ifstream file;

		string concatinate(string first, string second) {
			return first + second;
		}
};

string concatinate(string first, string second) { return first + second; }

string read(char* filename) {
	string line, lines = "";
	ifstream file;
	file.open(filename);
	if (file.is_open()) {
		while (file >> line) {
			lines = concatinate(lines, line);
		}
	} else {
		lines = "bad open";
	}
	file.close();
	return lines;
}