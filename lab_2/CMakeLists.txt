cmake_minimum_required(VERSION 3.10)

project(NIST_Generator_CPP)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(gen_cpp gen_cpp.cpp)