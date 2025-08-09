// Minimal entry point for aios_main
#include <iostream>

int main(int argc, char** argv)
{
	// Silence unused parameter warnings (treated as errors in build)
	(void)argc;
	(void)argv;
	std::cout << "AIOS Core main stub running." << std::endl;
	return 0;
}
