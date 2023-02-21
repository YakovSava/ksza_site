# include <string>
# include <fstream>
using namespace std;

class Writer {
	public:
		Writer(char* filename) {
			this->file.open(filename);
		};

		~Writer() {
			this->close()
		};

		void close() {
			if (this->file.is_open()) {
				this->file.close();
			}
		}

		void write(char* lines) {
			if (this->file.is_open()) {
				file << lines << endl;
			} else {
				this->close();
			}
		}

	private:
		ofstream file;
};

void write(char* filename, char* lines) {
	ofstream file;
	file.open(filename);
	if (file.is_open()) {
		file << lines << endl;
	}
	file.close();
}