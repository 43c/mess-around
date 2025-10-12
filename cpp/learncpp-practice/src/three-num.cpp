#include <iostream>

// Asks the user for three values (separated by spaces) and then prints
// these values as a sentence.
int main() {
	int x{}, y{}, z{};
	
	std::cout << "Enter three numbers (space separated): ";
	std::cin >> x;
	std::cin >> y;
	std::cin >> z;
	std::cout << "You entered " << x << ", " << y << " and " << z << ".\n";
	return 0;
}
