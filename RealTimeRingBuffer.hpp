// SPDX-License-Identifier: Apache-2.0
#ifndef REAL_TIME_RING_BUFFER_HPP
#define REAL_TIME_RING_BUFFER_HPP

#include <vector>
#include <atomic>
#include <stdexcept>

template<typename T>
class RealTimeRingBuffer {
private:
    std::vector<T> bufferMemory;
    size_t bufferCapacity;
    std::atomic<size_t> writeHead;
    std::atomic<size_t> readHead;

public:
    explicit RealTimeRingBuffer(size_t capacity = 1024)
        : bufferCapacity(capacity), writeHead(0), readHead(0) {
        if (capacity == 0) throw std::invalid_argument("capacity must be > 0");
        bufferMemory.resize(bufferCapacity);
    }

    RealTimeRingBuffer(const RealTimeRingBuffer&) = delete;
    RealTimeRingBuffer& operator=(const RealTimeRingBuffer&) = delete;

    bool push(const T& data) {
        size_t currentWrite = writeHead.load(std::memory_order_relaxed);
        size_t nextWrite = (currentWrite + 1) % bufferCapacity;
        if (nextWrite == readHead.load(std::memory_order_acquire)) {
            return false;
        }
        bufferMemory[currentWrite] = data;
        writeHead.store(nextWrite, std::memory_order_release);
        return true;
    }

    bool pop(T& output) {
        size_t currentRead = readHead.load(std::memory_order_relaxed);
        if (currentRead == writeHead.load(std::memory_order_acquire)) {
            return false;
        }
        output = bufferMemory[currentRead];
        readHead.store((currentRead + 1) % bufferCapacity, std::memory_order_release);
        return true;
    }

    size_t size() const {
        size_t write = writeHead.load(std::memory_order_acquire);
        size_t read = readHead.load(std::memory_order_acquire);
        if (write >= read) return write - read;
        return bufferCapacity - (read - write);
    }

    bool empty() const {
        return readHead.load(std::memory_order_acquire) == writeHead.load(std::memory_order_acquire);
    }

    bool full() const {
        size_t nextWrite = (writeHead.load(std::memory_order_acquire) + 1) % bufferCapacity;
        return nextWrite == readHead.load(std::memory_order_acquire);
    }

    size_t capacity() const { return bufferCapacity; }

    void reset() {
        writeHead.store(0, std::memory_order_release);
        readHead.store(0, std::memory_order_release);
    }
};

#endif
