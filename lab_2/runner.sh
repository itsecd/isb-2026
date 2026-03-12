#!/bin/bash

echo "Compiling C++ generator..."
g++ prng.cpp -o prng_cpp

echo "Compiling Java generator..."
javac prng.java

echo "Running generators..."

echo "C++..."
./prng_cpp 

echo "Python..."
python3 prng.py

echo "Java..."
java prng

echo "Cleaning temporary files..."

rm prng_cpp
rm prng.class

echo "Done."
