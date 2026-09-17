cmake_minimum_required(VERSION 3.14)
project(AMITY_OS VERSION 2.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find ZeroMQ (optional, for IPC Phase 3)
find_package(PkgConfig QUIET)
if(PkgConfig_FOUND)
    pkg_check_modules(ZMQ libzmq)
endif()

include_directories(include)

set(SOURCES
    src/AmitySovereigntyArtery.cpp
    src/AmityIpcClient.cpp
)

add_executable(amity_os ${SOURCES} src/main.cpp)

target_compile_options(amity_os PRIVATE -Wall -Wextra -O2)

if(ZMQ_FOUND)
    target_link_libraries(amity_os ${ZMQ_LIBRARIES})
    target_include_directories(amity_os PRIVATE ${ZMQ_INCLUDE_DIRS})
    target_compile_definitions(amity_os PRIVATE AMITY_IPC_ENABLED)
    message(STATUS "ZeroMQ found. IPC bridge enabled.")
else()
    message(STATUS "ZeroMQ NOT found. Build will compile without IPC bridge (stub mode).")
    message(STATUS "Install libzmq and cppzmq to enable Phase 3 IPC.")
endif()

# Install target
install(TARGETS amity_os DESTINATION bin)
