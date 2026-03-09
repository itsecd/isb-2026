cmake_minimum_required(VERSION 3.12)

project("task2" CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(${PROJECT_NAME} "task2.cpp")

target_compile_definitions(${PROJECT_NAME} PRIVATE 
    SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}")

if(CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang" OR
   CMAKE_CXX_COMPILER_ID STREQUAL "Clang" OR
   CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  target_compile_options(${PROJECT_NAME} PRIVATE "-Wall" "-Weffc++" "-Wextra" "-Wpedantic")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  if(CMAKE_CXX_FLAGS MATCHES "/W[0-4]")
    string(REGEX REPLACE "/W[0-4]" "" CMAKE_CXX_FLAGS ${CMAKE_CXX_FLAGS})
  endif()
  target_compile_options(${PROJECT_NAME} PRIVATE "/W4" "/utf-8")
endif()