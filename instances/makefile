all: cleaner

#### Problems 1 and 2

cleaner: cleaner.o
	g++ -std=c++11 cleaner.o -o cleaner

cleaner.o: cleaner.cpp
	g++ -std=c++11 -c cleaner.cpp

clean:
	rm *.o cleaner