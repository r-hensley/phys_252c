cmake_minimum_required(VERSION 3.21)
project(phys_252c)

set(CMAKE_CXX_STANDARD 14)

include_directories("HW/HW3")

add_executable(phys_252c
        HW/HW1/problem_5.cpp
        HW/HW3/problem_4/problem_4.cpp
        HW/HW3/problem_4/problem_5.cpp)

include_directories("~/root/include")

