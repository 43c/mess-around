# Invokes 'make clean' in every immediate sub-directory
# before we push.
# 
# Sub-directories should have their own clean handling.

# Running "ls */" gives information about every directory
# AND their contents. Adding the "-d" flags returns only
# the directories.
SUB_DIRS := $(shell ls -d */)

.PHONY: clean $(SUB_DIRS)

$(SUB_DIRS):
	@$(MAKE) -C $@ $(MAKECMDGOALS)

clean: $(SUB_DIRS)
