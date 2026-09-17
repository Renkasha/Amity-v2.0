// SPDX-License-Identifier: Apache-2.0
#ifndef AMITY_IPC_CLIENT_HPP
#define AMITY_IPC_CLIENT_HPP

#include <string>
#include <functional>
#include <thread>
#include <atomic>

// Minimal forward-declare for zmq if available; otherwise stub
#ifdef AMITY_IPC_ENABLED
#include <zmq.hpp>
#endif

namespace amity {

struct IpcMessage {
    std::string type;
    std::string jsonPayload;
};

class AmityIpcClient {
public:
    AmityIpcClient();
    ~AmityIpcClient();

    bool connect(const std::string& telemetryAddr = "tcp://127.0.0.1:5555",
                 const std::string& commandAddr = "tcp://127.0.0.1:5556");
    void disconnect();
    bool isConnected() const;

    // Subscribe to telemetry from Python
    bool receiveTelemetry(IpcMessage& out);

    // Send status back to Python
    void sendStatus(const std::string& jsonStatus);

private:
    std::atomic<bool> connected;
#ifdef AMITY_IPC_ENABLED
    zmq::context_t* context;
    zmq::socket_t* telemetrySub;
    zmq::socket_t* commandReq;
#else
    void* dummy;
#endif
};

}

#endif
