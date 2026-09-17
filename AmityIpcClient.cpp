// SPDX-License-Identifier: Apache-2.0
#include "AmityIpcClient.hpp"
#include <iostream>

namespace amity {

#ifdef AMITY_IPC_ENABLED

AmityIpcClient::AmityIpcClient()
    : connected(false), context(nullptr), telemetrySub(nullptr), commandReq(nullptr) {}

AmityIpcClient::~AmityIpcClient() {
    disconnect();
}

bool AmityIpcClient::connect(const std::string& telemetryAddr,
                             const std::string& commandAddr) {
    try {
        context = new zmq::context_t(1);
        telemetrySub = new zmq::socket_t(*context, ZMQ_SUB);
        telemetrySub->connect(telemetryAddr);
        telemetrySub->setsockopt(ZMQ_SUBSCRIBE, "", 0);
        telemetrySub->setsockopt(ZMQ_RCVTIMEO, 500);

        commandReq = new zmq::socket_t(*context, ZMQ_REQ);
        commandReq->connect(commandAddr);
        commandReq->setsockopt(ZMQ_RCVTIMEO, 500);

        connected.store(true);
        return true;
    } catch (const std::exception& e) {
        std::cerr << "[IPC] Connect failed: " << e.what() << std::endl;
        disconnect();
        return false;
    }
}

void AmityIpcClient::disconnect() {
    connected.store(false);
    if (telemetrySub) { telemetrySub->close(); delete telemetrySub; telemetrySub = nullptr; }
    if (commandReq) { commandReq->close(); delete commandReq; commandReq = nullptr; }
    if (context) { context->close(); delete context; context = nullptr; }
}

bool AmityIpcClient::isConnected() const {
    return connected.load();
}

bool AmityIpcClient::receiveTelemetry(IpcMessage& out) {
    if (!connected.load() || !telemetrySub) return false;
    zmq::message_t msg;
    try {
        if (telemetrySub->recv(&msg)) {
            out.type = "telemetry";
            out.jsonPayload = std::string(static_cast<char*>(msg.data()), msg.size());
            return true;
        }
    } catch (...) {}
    return false;
}

void AmityIpcClient::sendStatus(const std::string& jsonStatus) {
    if (!connected.load() || !commandReq) return;
    try {
        zmq::message_t req(jsonStatus.size());
        memcpy(req.data(), jsonStatus.data(), jsonStatus.size());
        commandReq->send(req);
        zmq::message_t reply;
        commandReq->recv(&reply);
    } catch (...) {}
}

#else // No ZeroMQ: stub implementation

AmityIpcClient::AmityIpcClient() : connected(false), dummy(nullptr) {}
AmityIpcClient::~AmityIpcClient() {}
bool AmityIpcClient::connect(const std::string&, const std::string&) {
    std::cerr << "[IPC] ZeroMQ not available. Build with -DAMITY_IPC_ENABLED and link libzmq." << std::endl;
    return false;
}
void AmityIpcClient::disconnect() {}
bool AmityIpcClient::isConnected() const { return false; }
bool AmityIpcClient::receiveTelemetry(IpcMessage&) { return false; }
void AmityIpcClient::sendStatus(const std::string&) {}

#endif

}
