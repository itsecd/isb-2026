#!/bin/bash

echo "Compiling C++ generator..."
g++ prng.cpp -o prng_cpp

echo "Compiling Java generator..."
javac Generator.java

echo "Running generators..."

echo "C++..."
./prng_cpp 

echo "Python..."
python3 prng.py

echo "Java..."
java Generator

echo "Cleaning temporary files..."

rm prng_cpp
rm Generator.class

echo "Done."
