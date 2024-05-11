CC = clang # Compiler used
CFLAGS = -Wall -std=c99 -pedantic -fPIC # Compiler flags, added -fPIC for all compilations
PYTHON_VERSION = 3.11
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION) # Python include path
PYTHON_LIB = /usr/lib/python$(PYTHON_VERSION) # Python lib path

# Main target
all: _phylib.so 

# Clean all the files produced by make
clean: cleanAll	#FOR REGRADE: Simplified what is being cleaned, I am not sure if this would effect the autograder
	rm -f *.o *.so *.exe

cleanSvgs: 
	rm -f *.svg

cleand:
	rm -f *.db	

cleanAll: cleand cleanSvgs
	rm -f phylib_wrap.c phylib.py -r __pycache__ phylib.db
#FOR REGRADE: "I had an executable called myprog from a1, which was not necessary"

# Compile .c and .h files
phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o	

# This builds the shared library	
libphylib.so: phylib.o #FOR REGRADE: The target was previously 'phylib.so' not 'libphylib.so'. 
	$(CC) -shared -o libphylib.so phylib.o -lm

# This target will generate the SWIG wrapper files phylib_wrap.c and phylib.py
phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

# Compile SWIG wrapper
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -fPIC -I$(PYTHON_INCLUDE) -o phylib_wrap.o

# Build Python shared library
_phylib.so: phylib_wrap.o libphylib.so # FOR REGARDE: one of the targets was 'libphylib.so' instead of 'libphylib.so' 
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L$(PYTHON_LIB) -lpython$(PYTHON_VERSION) -lphylib -o _phylib.so 
	
# apparently -shared works for linux too






