cmake_minimum_required(VERSION 3.10)
project(SortingProject)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(main main.cpp)

target_include_directories(main PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

if (MSVC)
	target_compile_options(main PRIVATE /W4 /WX)
else()
	target_compile_options(main PRIVATE -Wall -Wextra -Wpedantic -Wconversion)
endif()