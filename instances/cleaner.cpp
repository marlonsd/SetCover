#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <cstring>
#include <cstdlib>
#include <deque>
#include <algorithm>
#include <functional>
#include <unordered_set>
#include <dirent.h>
#include <unordered_map> // C++11 Hash Table
#include <chrono> // C++11 Time lib

using namespace std::chrono;
using namespace std;

vector<string> list_dir_files(string path);

int main(int argc, char* argv[]){
	string dir_path = "raw/";
	string filename, out_filename, s, token, final_string;

	fstream input, output;

	vector<string> files = list_dir_files(dir_path);

	for (string file : files){
		filename = dir_path + file;
		out_filename = "clean/" + file;

		input.open(filename, ios::in);
		output.open(out_filename, ios::out);

		final_string = "";

		if (input.is_open() && output.is_open()){
			int n, m, p;

			input >> n >> m;

			output << n << " " << m << "\n";

			for (int i = 0; i < m; ++i){
				input >> s;
			}

			for (int i = 0; i < n; ++i){
				input >> p;

				for (int j = 0; j < p; ++j){
					input >> s;
					final_string += (s + " ");
				}

				final_string.pop_back();

				final_string += "\n";
			}

			final_string.pop_back();
		}

		output << final_string;

		input.close();
		output.close();

	}

}

vector<string> list_dir_files(string path) {

	DIR* dir;
	dirent* pdir;
	vector<std::string> files;

	dir = opendir(path.c_str());

	while ((pdir = readdir(dir))){
		string filename = pdir->d_name;
		if (filename != "." && filename != ".." && filename[0] != '.'){
			files.push_back(filename);
		}
	}

	closedir(dir);

	sort(files.begin(), files.end());

	return files;
}