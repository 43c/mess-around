CXX := g++
PEDANTIC_FLAGS := -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -pedantic
STRICT_FLAGS := -Werror -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -pedantic-errors
hello : hello.cpp
	$(CXX) $(PEDANTIC_FLAGS) -o hello hello.cpp

strict : hello.cpp
	$(CXX) $(STRICT_FLAGS) -o hello hello.cpp

clean : 
	-rm hello
