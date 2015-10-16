// Copyright © 2015 Martin Ueding <dev@martin-ueding.de>

#include <chrono>
#include <fstream>
#include <iostream>
#include <thread>
#include <vector>

template <typename Number>
void fib(const long max) {
    Number a = 1;
    Number b = 1;
    for (long i = 0; i != max; ++i) {
        const Number c = a + b;
        a = b;
        b = c;
    }

    std::cout << b << std::endl;
}

template <typename Number> std::string name();

template <> std::string name<double>() {
    return "double";
}

template <> std::string name<int>() {
    return "int";
}

template <> std::string name<long long>() {
    return "long-long";
}

template <> std::string name<float>() {
    return "float";
}

template <typename Number> void take_measurement() {
    std::ofstream out{"data-" + name<Number>() + ".txt"};
    for (int thread_count = 1;
         thread_count <= 2 * std::thread::hardware_concurrency();
         ++thread_count) {
        auto start_time = std::chrono::steady_clock::now();
        std::vector<std::thread> threads;

        for (int thread_id = 0; thread_id != thread_count; ++thread_id) {
            threads.push_back(std::thread{[] { fib<Number>(2000000000L); }});
        }

        for (auto &thread : threads) {
            thread.join();
        }

        auto duration =
            std::chrono::duration_cast<std::chrono::milliseconds>(
                std::chrono::steady_clock::now() - start_time).count() /
            1000.0;

        std::cerr << "Threads: " << thread_count
                  << ", Max-Duration: " << duration << std::endl;
        out << thread_count << "\t" << duration << "\n";
    }
}

int main(int argc, char **argv) {
    take_measurement<int>();
    take_measurement<long long>();
    take_measurement<double>();
    take_measurement<float>();

    return 0;
}
