// SPDX-License-Identifier: Apache-2.0
#ifndef AMITY_INGRESS_QUEUE_HPP
#define AMITY_INGRESS_QUEUE_HPP

#include <queue>
#include <string>
#include <cstdint>
#include <iostream>

namespace amity {

struct IngressRequest {
    uint32_t requestId;
    std::string originBlock;
    int priorityLevel;
    double payloadTimestamp;
};

struct PriorityComparator {
    bool operator()(const IngressRequest& a, const IngressRequest& b) {
        return a.priorityLevel < b.priorityLevel;
    }
};

class AmityIngressMonitoringSystem {
private:
    std::priority_queue<IngressRequest, std::vector<IngressRequest>, PriorityComparator> requestQueue;
    uint32_t totalProcessedPackets;

public:
    AmityIngressMonitoringSystem() : totalProcessedPackets(0) {}

    void pushToIngressQueue(uint32_t id, const std::string& block, int tier) {
        IngressRequest req{id, block, tier, 0.0};
        requestQueue.push(req);
        std::cout << "[API-GATEWAY]: Intercepted stream payload [" << id << "] -> Tier-" << tier << " Buffer." << std::endl;
    }

    void flushQueueToMatrixController() {
        std::cout << "\n[MATRIX-CONTROLLER]: Processing incoming queue streams by priority..." << std::endl;
        while (!requestQueue.empty()) {
            IngressRequest activeReq = requestQueue.top();
            std::cout << "  Processing Packet [" << activeReq.requestId << "] from Sector: "
                      << activeReq.originBlock << " | [Tier: " << activeReq.priorityLevel << "]" << std::endl;
            totalProcessedPackets++;
            requestQueue.pop();
        }
        std::cout << "[STATS-DB]: Telemetry logs written." << std::endl;
    }

    uint32_t getProcessedCount() const { return totalProcessedPackets; }
};

}

#endif
