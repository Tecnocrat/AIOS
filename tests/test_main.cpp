#include <iostream>
#include <sstream>
#include <cassert>

void test_hello_aios() {
    std::ostringstream output;
    output << "Hello, AI OS";
    assert(output.str() == "Hello, AI OS");
    std::cout << "Test passed: Hello, AI OS" << std::endl;
}

int main() {
    test_hello_aios();
    return 0;
}