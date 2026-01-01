// Minimal entry point for aios_main
#include <iostream>
#include "aios_core_minimal.hpp"

int main(int argc, char** argv) {
	(void)argc; (void)argv;
	std::cout << "AIOS Core main with telemetry." << std::endl;
	aios::Core core;
	if(core.initialize()) {
		core.start();
		// Run brief loop to allow telemetry thread to emit samples
		std::this_thread::sleep_for(std::chrono::seconds(3));
		core.stop();
	}
	return 0;
}
