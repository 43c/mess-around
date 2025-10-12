# Makefile for a learning setup. Builds one binary for each source files.
#
# 'make' will find all .cpp in the $SRC_DIR folder, compile them into
# object files in the $BUILD_DIR folder, and finally output individual
# executables for each source file.
CXX := g++

# COMPILATION PHASE FLAGS
# Pedantic flags for many warnings.
# Strict flags will cause error instead of warnings.
PEDANTIC_FLAGS := -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -pedantic
STRICT_FLAGS := -Werror -Wall -Weffc++ -Wextra -Wconversion -Wsign-conversion -pedantic-errors

# LINK PHASE FLAGS
CPP_LINK_FLAGS := 

# SRC_DIR: Directory of source files.
# BUILD_DIR: Directory of intermediate files.
# BIN_DIR: Directory of output executables.
SRC_DIR := src
BUILD_DIR := build
BIN_DIR := bin

# We mark the .o files as secondary as some implicit
# Collect all the files into easily referenced names.
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)
BINS := $(SRCS:$(SRC_DIR)/%.cpp=$(BIN_DIR)/%)

# We mark .o files as ".SECONDARY" so they don't get cleaned up,
# and will be left in $BUILD_DIR. Make seems to hav some automatic 
# mechanism to clean up intermediate files after executing
.SECONDARY: $(OBJS)

all: $(BINS)

# Fallback rule for when I want to only build one binary.
%: $(BIN_DIR)/%
# This pattern will not work without adding the belwo null
# command. Without the null comand, Make checks this rule,
# and sees that no file named % exists. But, it also sees
# that this rule has no command. Make determines that this
# target cannot be made, and will warn "No rule to make target"
	@:

# Implicit rules (pattern rules).
$(BIN_DIR)/%: $(BUILD_DIR)/%.o
	@mkdir -p $(BIN_DIR)
	$(CXX) $< -o $@

$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	$(CXX) $(PEDANTIC_FLAGS) $< -c -o $@

# This ensures that clean is not a physical target, so if we have a physical
# file "clean", make will still run 'make clean' and not say that clean is 
# already up to date.
.PHONY: clean

clean:
	@rm -rf $(BUILD_DIR) $(BIN_DIR)
