cmake_minimum_required(VERSION 3.12)
project("ISB_Lab2_generator" CXX)
add_executable("ISB_Lab2_generator" 
"generator_cpp.cpp")

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

if(CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang" OR
   CMAKE_CXX_COMPILER_ID STREQUAL "Clang" OR
   CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
   add_compile_options("-Wall" "-Weffc++" "-Wextra" "-Wpedantic")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "" CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
  endif()
  add_compile_options("/W4" "/utf-8")
endif()

