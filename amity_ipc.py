"""AMITY IPC Bridge v2.0
ZeroMQ PUB/SUB telemetry stream + REQ/REP command channel
Python Sovereign -> C++ Firmware
"""
import json
import time
import threading
import logging
from typing import Optional, Dict, Any, Callable

try:
    import zmq
except ImportError:
    raise ImportError("pyzmq required for IPC bridge. Install: pip install pyzmq")

logger = logging.getLogger(__name__)


class ZmqPublisher:
    """Publishes SensorReading telemetry to C++ firmware."""
    def __init__(self, telemetry_port=5555, command_port=5556):
        self.context = zmq.Context()
        self.telemetry_socket = self.context.socket(zmq.PUB)
        self.telemetry_socket.bind(f"tcp://127.0.0.1:{telemetry_port}")
        self.command_socket = self.context.socket(zmq.REP)
        self.command_socket.bind(f"tcp://127.0.0.1:{command_port}")
        self._lock = threading.Lock()
        self._running = True
        self._command_thread = threading.Thread(target=self._command_loop, daemon=True)
        self._command_thread.start()
        # Warmup: PUB sockets need time before subscribers see messages
        time.sleep(0.2)
        logger.info("ZmqPublisher bound: telemetry=%s, command=%s", telemetry_port, command_port)

    def publish_sensory(self, reading: Dict[str, Any]):
        msg = {
            "type": "sensory_reading",
            "payload": reading,
        }
        with self._lock:
            self.telemetry_socket.send_string(json.dumps(msg))

    def publish_command(self, action: str, params: Optional[Dict] = None):
        msg = {
            "type": "command",
            "action": action,
            "params": params or {},
        }
        with self._lock:
            self.telemetry_socket.send_string(json.dumps(msg))

    def _command_loop(self):
        """Handle status requests from C++ firmware."""
        while self._running:
            try:
                self.command_socket.RCVTIMEO = 500
                req = self.command_socket.recv_string()
                data = json.loads(req)
                resp = {"type": "status", "ack": True, "received": data.get("type", "unknown")}
                self.command_socket.send_string(json.dumps(resp))
            except zmq.Again:
                continue
            except Exception as e:
                logger.debug("Command loop error: %s", e)

    def close(self):
        self._running = False
        self.telemetry_socket.close()
        self.command_socket.close()
        self.context.term()


class ZmqCommandServer:
    """Receives status updates from C++ firmware."""
    def __init__(self, status_port=5557):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://127.0.0.1:{status_port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self._callbacks: list[Callable[[Dict], None]] = []
        self._running = True
        self._thread = threading.Thread(target=self._recv_loop, daemon=True)
        self._thread.start()
        logger.info("ZmqCommandServer connected to C++ status on port %s", status_port)

    def on_status(self, callback: Callable[[Dict], None]):
        self._callbacks.append(callback)

    def _recv_loop(self):
        while self._running:
            try:
                self.socket.RCVTIMEO = 500
                msg = self.socket.recv_string()
                data = json.loads(msg)
                for cb in self._callbacks:
                    try:
                        cb(data)
                    except Exception:
                        logger.exception("Status callback failed")
            except zmq.Again:
                continue
            except Exception as e:
                logger.debug("Recv loop error: %s", e)

    def close(self):
        self._running = False
        self.socket.close()
        self.context.term()


class AmityIpcBridge:
    """Unified IPC facade for SessionManager."""
    def __init__(self, session_manager, telemetry_port=5555, command_port=5556, status_port=5557):
        self.sm = session_manager
        self.pub = ZmqPublisher(telemetry_port, command_port)
        self.sub = ZmqCommandServer(status_port)
        self.sub.on_status(self._handle_status)

    def _handle_status(self, status: Dict):
        if status.get("type") == "status":
            sector = status.get("sector", "unknown")
            energy = status.get("energy_level", 1.0)
            boundary = status.get("boundary_active", False)
            pressure = status.get("buffer_pressure", 0.0)
            logger.info("[IPC] C++ status: sector=%s energy=%.2f boundary=%s pressure=%.2f",
                        sector, energy, boundary, pressure)
            # If C++ reports high pressure, throttle Python side
            if pressure > 0.9:
                self.sm.heart.throttle_flag = True

    def heartbeat(self, payload, origin, priority=0):
        result = self.sm.heart.heartbeat(payload, origin, priority)
        # Stream sensory data to C++ if this is a sensory beat
        if origin == "sensory" and "friction" in payload:
            self.pub.publish_sensory(payload)
        return result

    def close(self):
        self.pub.close()
        self.sub.close()
