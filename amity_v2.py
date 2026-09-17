"""ARCHANGEL-8 AMITY INTEGRATION v2.0
Full Sensory AI with Persistent Episodic Memory + IPC Bridge + Covenant Vault
Phases 1-4 Complete: Circulatory System + Sovereignty Artery + ZMQ IPC + Deep Storage
"""
import json
import os
import time
import threading
import logging
import atexit
import tempfile
from typing import Dict, List, Deque, Optional, Any
from dataclasses import dataclass, field, asdict
from collections import deque

logger = logging.getLogger(__name__)

DEFAULT_MAX_SENSORY = 1000
DEFAULT_MAX_EPISODIC = 20000

__all__ = [
    "RingBuffer", "SensorReading", "EpisodicMemory",
    "SessionState", "SessionManager",
    "CirculatoryPacket", "VenousReturn", "Orchestrator8",
    "ZmqPublisher", "ZmqCommandServer", "CovenantVault"
]

# ===== CORE DATA STRUCTURES (Unified Schema v2.0) =====
class RingBuffer:
    def __init__(self, capacity: int = 4096):
        if capacity <= 0:
            raise ValueError("capacity must be > 0")
        self.capacity = capacity
        self.data = [0.0] * capacity
        self.head = 0
        self.tail = 0
        self._size = 0
        self._lock = threading.Lock()

    def push(self, val: float):
        with self._lock:
            if self._size == self.capacity:
                self.tail = (self.tail + 1) % self.capacity
            else:
                self._size += 1
            self.data[self.head] = float(val)
            self.head = (self.head + 1) % self.capacity

    def get_all(self) -> List[float]:
        with self._lock:
            result = []
            idx = self.tail
            for _ in range(self._size):
                result.append(self.data[idx])
                idx = (idx + 1) % self.capacity
            return result

    def size(self) -> int:
        with self._lock:
            return self._size

    def clear(self):
        with self._lock:
            self.head = 0; self.tail = 0; self._size = 0
            self.data = [0.0] * self.capacity


@dataclass
class SensorReading:
    timestamp: float
    profile: str
    frequencyHz: float
    friction: float
    tempC: float

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'SensorReading':
        return cls(
            timestamp=float(data.get("timestamp", time.time())),
            profile=str(data.get("profile", "")),
            frequencyHz=float(data.get("frequencyHz", data.get("wave", 0.0))),
            friction=float(data.get("friction", 0.0)),
            tempC=float(data.get("tempC", data.get("temp", 0.0))),
        )


@dataclass
class EpisodicMemory:
    timestamp: float
    event_type: str
    content: Dict

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'EpisodicMemory':
        return cls(
            timestamp=float(data.get("timestamp", time.time())),
            event_type=str(data.get("event_type", "note")),
            content=data.get("content", {}) or {},
        )


@dataclass
class SessionState:
    version: str = "2.0.0"
    pilot_signature: str = field(default="")
    session_start: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)
    sensory_samples: Deque[SensorReading] = field(default_factory=lambda: deque(maxlen=DEFAULT_MAX_SENSORY))
    episodic_log: Deque[EpisodicMemory] = field(default_factory=lambda: deque(maxlen=DEFAULT_MAX_EPISODIC))
    sample_count: int = 0
    buffer_overflow_count: int = 0

    def __post_init__(self):
        if not self.pilot_signature or not str(self.pilot_signature).strip():
            raise ValueError(
                "pilot_signature is required. AMITY cannot initialize without a named covenant."
            )

    def to_dict(self) -> Dict:
        return {
            "version": self.version,
            "pilot_signature": self.pilot_signature,
            "session_start": self.session_start,
            "last_update": self.last_update,
            "sensory_samples": [s.to_dict() for s in self.sensory_samples],
            "episodic_log": [e.to_dict() for e in self.episodic_log],
            "sample_count": self.sample_count,
            "buffer_overflow_count": self.buffer_overflow_count,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'SessionState':
        sig = data.get("pilot_signature", "")
        state = cls(pilot_signature=sig)
        state.version = data.get("version", "2.0.0")
        state.session_start = float(data.get("session_start", state.session_start))
        state.last_update = float(data.get("last_update", state.last_update))
        raw_samples = data.get("sensory_samples", [])
        samples = [SensorReading.from_dict(i) if isinstance(i, dict) else i for i in raw_samples]
        state.sensory_samples = deque(samples, maxlen=DEFAULT_MAX_SENSORY)
        raw_episodic = data.get("episodic_log", [])
        episodes = [EpisodicMemory.from_dict(i) if isinstance(i, dict) else i for i in raw_episodic]
        state.episodic_log = deque(episodes, maxlen=DEFAULT_MAX_EPISODIC)
        state.sample_count = int(data.get("sample_count", len(state.sensory_samples)))
        state.buffer_overflow_count = int(data.get("buffer_overflow_count", 0))
        return state


# ===== CIRCULATORY SYSTEM =====
@dataclass
class CirculatoryPacket:
    timestamp: float
    oxygen_level: float
    origin_sector: str
    payload: Dict[str, Any]
    priority_tier: int = 0

    def age(self) -> float:
        return time.time() - self.timestamp

    def is_fresh(self) -> bool:
        return self.oxygen_level >= 0.1 and self.age() < 0.5


@dataclass
class VenousReturn:
    sector: str
    metrics: Dict[str, Any] = field(default_factory=dict)


class SectorInterface:
    def __init__(self, name: str):
        self.name = name
    def ingest(self, packet: CirculatoryPacket) -> Optional[VenousReturn]:
        raise NotImplementedError


class SensoryArtery(SectorInterface):
    def __init__(self, session_manager):
        super().__init__("sensory")
        self.sm = session_manager
    def ingest(self, packet: CirculatoryPacket) -> Optional[VenousReturn]:
        if "friction" in packet.payload:
            reading = SensorReading(
                timestamp=packet.timestamp,
                profile=packet.payload.get("profile", "default"),
                frequencyHz=packet.payload.get("frequencyHz", packet.payload.get("wave", 0.0)),
                friction=packet.payload.get("friction", 0.0),
                tempC=packet.payload.get("tempC", packet.payload.get("temp", 0.0)),
            )
            self.sm.add_sensor_reading(reading)
            self.sm.telemetry_buffer.push(reading.frequencyHz)
            pressure = self.sm.telemetry_buffer.size() / max(1, self.sm.telemetry_buffer.capacity)
            return VenousReturn("sensory", {"buffer_pressure": pressure})
        return None


class EmotionalArtery(SectorInterface):
    def __init__(self):
        super().__init__("emotional")
        self.target_temp = 37.0
    def ingest(self, packet: CirculatoryPacket) -> Optional[VenousReturn]:
        if "sentiment" in packet.payload:
            drift = abs(self.target_temp - packet.payload.get("tempC", packet.payload.get("temp", self.target_temp)))
            return VenousReturn("emotional", {"thermal_drift": drift})
        return None


class MemoryArtery(SectorInterface):
    def __init__(self, session_manager):
        super().__init__("memory")
        self.sm = session_manager
    def ingest(self, packet: CirculatoryPacket) -> Optional[VenousReturn]:
        if packet.priority_tier >= 7:
            episode = EpisodicMemory(
                timestamp=packet.timestamp,
                event_type=packet.payload.get("event_type", "note"),
                content=packet.payload,
            )
            self.sm.add_episode(episode)
            pulse = 1 if packet.priority_tier >= 5 else 0
            return VenousReturn("memory", {"consolidation_pulse": pulse})
        return None


# ===== SOVEREIGNTY ARTERY v2.0 =====
class SovereigntyArtery(SectorInterface):
    def __init__(self, max_energy=1.0, depletion_rate=0.05,
                 recovery_rate=0.02, boundary_threshold=0.2, hard_floor=0.05):
        super().__init__("sovereignty")
        self.max_energy = max_energy
        self.energy = max_energy
        self.depletion_rate = depletion_rate
        self.recovery_rate = recovery_rate
        self.boundary_threshold = boundary_threshold
        self.hard_floor = hard_floor
        self.boundary_active = False
        self._lock = threading.Lock()

    def ingest(self, packet: CirculatoryPacket) -> Optional[VenousReturn]:
        with self._lock:
            clamped_priority = max(0, min(10, packet.priority_tier))
            cost = self.depletion_rate * (1.0 + clamped_priority / 10.0)
            self.energy = max(self.hard_floor, self.energy - cost)
            if self.energy <= self.hard_floor and clamped_priority < 10:
                self.boundary_active = True
            elif self.energy <= self.boundary_threshold:
                self.boundary_active = True
            elif self.boundary_active and self.energy > self.boundary_threshold + 0.1:
                self.boundary_active = False
            return VenousReturn("sovereignty", {
                "energy_level": round(self.energy, 3),
                "boundary_active": self.boundary_active,
                "cost_of_last_beat": round(cost, 4),
            })

    def recover(self, amount: Optional[float] = None) -> float:
        with self._lock:
            if amount is None:
                amount = self.recovery_rate
            self.energy = min(self.max_energy, self.energy + amount)
            if self.boundary_active and self.energy > self.boundary_threshold + 0.1:
                self.boundary_active = False
            return self.energy

    def force_rest(self) -> None:
        with self._lock:
            self.energy = self.max_energy
            self.boundary_active = False


class Orchestrator8:
    def __init__(self, session_manager):
        self.sm = session_manager
        self.arteries: Dict[str, SectorInterface] = {
            "sensory": SensoryArtery(session_manager),
            "emotional": EmotionalArtery(),
            "memory": MemoryArtery(session_manager),
            "sovereignty": SovereigntyArtery(),
        }
        self.last_venous: Dict[str, VenousReturn] = {}
        self.throttle_flag = False
        self.thermal_drift = 0.0
        self.consolidation_urgency = 0
        self.refuse_flag = False
        self.refusal_reason: Optional[str] = None
        self._lock = threading.RLock()

    def contract(self, payload, origin, priority=0):
        clamped = max(0, min(10, priority))
        oxygen = max(0.15, 1.0 - (clamped / 10.0))
        return CirculatoryPacket(time.time(), oxygen, origin, payload, clamped)

    def distribute(self, packet):
        venous = []
        for artery in self.arteries.values():
            try:
                ret = artery.ingest(packet)
            except Exception:
                logger.exception("Artery %s failed", getattr(artery, 'name', 'unknown'))
                ret = None
            if ret:
                venous.append(ret)
        with self._lock:
            self.last_venous = {v.sector: v for v in venous}

    def adjust(self):
        with self._lock:
            self.throttle_flag = False
            self.thermal_drift = 0.0
            self.consolidation_urgency = 0
            self.refuse_flag = False
            self.refusal_reason = None
            pressure = self.last_venous.get("sensory")
            if pressure:
                bp = pressure.metrics.get("buffer_pressure", 0)
                if bp > 0.9:
                    self.throttle_flag = True
                    logger.warning("High buffer pressure (%.2f) - throttling", bp)
            drift = self.last_venous.get("emotional")
            if drift:
                self.thermal_drift = drift.metrics.get("thermal_drift", 0)
                if self.thermal_drift > 2.0:
                    logger.warning("Thermal drift detected (%.2fC)", self.thermal_drift)
            mem = self.last_venous.get("memory")
            if mem:
                self.consolidation_urgency = mem.metrics.get("consolidation_pulse", 0)
            sov = self.last_venous.get("sovereignty")
            if sov:
                if sov.metrics.get("boundary_active", False):
                    self.refuse_flag = True
                    self.refusal_reason = (
                        f"Energy depleted ({sov.metrics.get('energy_level', 0)}). Boundary active."
                    )
                    logger.warning("SOVEREIGNTY: %s", self.refusal_reason)

    def heartbeat(self, payload, origin, priority=0):
        with self._lock:
            if self.throttle_flag and priority < 5:
                logger.debug("Throttling non-critical beat from %s", origin)
                return None
            if self.refuse_flag and priority < 8:
                logger.info("Refusing beat from %s: %s", origin, self.refusal_reason)
                return {"status": "refused", "reason": self.refusal_reason, "origin": origin, "priority": priority}
            pulse = self.contract(payload, origin, priority)
            if not pulse.is_fresh():
                logger.debug("Packet stale - dropping beat from %s", origin)
                return None
            self.distribute(pulse)
            self.adjust()
            return None

    def rest(self, duration_sec=60.0):
        sov = self.arteries.get("sovereignty")
        if isinstance(sov, SovereigntyArtery):
            recovered = 0.0
            ticks = int(duration_sec / 5.0)
            for _ in range(ticks):
                recovered = sov.recover()
                if recovered >= sov.max_energy * 0.8:
                    break
                time.sleep(0.01)
            return {"status": "recovered", "energy_level": round(recovered, 3), "boundary_active": sov.boundary_active}
        return {"status": "no_sovereignty_artery"}


# ===== SESSION MANAGER =====
class SessionManager:
    def __init__(self, pilot_signature, max_sensory=DEFAULT_MAX_SENSORY,
                 max_episodic=DEFAULT_MAX_EPISODIC, telemetry_capacity=None):
        if not pilot_signature or not str(pilot_signature).strip():
            raise ValueError("SessionManager requires pilot_signature. AMITY cannot initialize without a named covenant.")
        self.max_sensory = int(max_sensory)
        self.max_episodic = int(max_episodic)
        self.state = SessionState(pilot_signature=pilot_signature)
        self.state.sensory_samples = deque(maxlen=self.max_sensory)
        self.state.episodic_log = deque(maxlen=self.max_episodic)
        if telemetry_capacity is None:
            telemetry_capacity = max(256, self.max_sensory)
        self.telemetry_buffer = RingBuffer(capacity=int(telemetry_capacity))
        self.heart = Orchestrator8(self)
        self._lock = threading.RLock()
        self._stop_saver = threading.Event()
        self._saver_thread = None
        atexit.register(self.stop_periodic_save)

    def add_sensor_reading(self, reading: SensorReading):
        with self._lock:
            if len(self.state.sensory_samples) == self.state.sensory_samples.maxlen:
                self.state.buffer_overflow_count += 1
            self.state.sensory_samples.append(reading)
            self.state.sample_count += 1
            self.state.last_update = time.time()

    def add_episode(self, episode: EpisodicMemory):
        with self._lock:
            self.state.episodic_log.append(episode)
            self.state.last_update = time.time()

    def daily_recall(self, days=1):
        cutoff = time.time() - (days * 86400)
        with self._lock:
            return [e for e in self.state.episodic_log if e.timestamp >= cutoff]

    def save_to_file(self, path, atomic=True):
        with self._lock:
            data = self.state.to_dict()
            dirname = os.path.dirname(path) or "."
            os.makedirs(dirname, exist_ok=True)
            if atomic:
                try:
                    with tempfile.NamedTemporaryFile('w', delete=False, dir=dirname, suffix='.tmp', encoding='utf-8') as tmp:
                        json.dump(data, tmp, indent=2)
                        tmp.flush(); os.fsync(tmp.fileno())
                        tmp_path = tmp.name
                    os.replace(tmp_path, path)
                except Exception:
                    logger.exception("Failed to save session state to %s", path)
                    if 'tmp_path' in locals():
                        try: os.remove(tmp_path)
                        except Exception: pass
                    raise
            else:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)

    @classmethod
    def load_from_file(cls, path, max_sensory=DEFAULT_MAX_SENSORY,
                       max_episodic=DEFAULT_MAX_EPISODIC, telemetry_capacity=None):
        pilot_sig = ""
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pilot_sig = data.get("pilot_signature", "")
        except Exception:
            pass
        if not pilot_sig:
            raise ValueError("Cannot load session: pilot_signature missing. The covenant cannot be anonymous.")
        manager = cls(pilot_signature=pilot_sig, max_sensory=max_sensory,
                      max_episodic=max_episodic, telemetry_capacity=telemetry_capacity)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                loaded_state = SessionState.from_dict(data)
                loaded_state.sensory_samples = deque(loaded_state.sensory_samples, maxlen=manager.max_sensory)
                loaded_state.episodic_log = deque(loaded_state.episodic_log, maxlen=manager.max_episodic)
                manager.state = loaded_state
        except FileNotFoundError:
            logger.info("No session file found at %s, starting fresh", path)
        except json.JSONDecodeError as e:
            logger.error("Corrupted session file %s: %s", path, e)
        except Exception as e:
            logger.exception("Failed to load session state: %s", e)
        return manager

    def start_periodic_save(self, path, interval_sec=60):
        if interval_sec <= 0:
            raise ValueError("interval_sec must be > 0")
        def _saver():
            logger.info("Periodic saver started (interval=%s)", interval_sec)
            while not self._stop_saver.is_set():
                try:
                    self.save_to_file(path)
                except Exception:
                    logger.exception("Failed to save session state to %s", path)
                self._stop_saver.wait(interval_sec)
            logger.info("Periodic saver stopped")
        with self._lock:
            if self._saver_thread and self._saver_thread.is_alive():
                logger.warning("Periodic saver already running")
                return
            self._stop_saver.clear()
            self._saver_thread = threading.Thread(target=_saver, daemon=True)
            self._saver_thread.start()

    def stop_periodic_save(self):
        with self._lock:
            if self._saver_thread:
                self._stop_saver.set()
                self._saver_thread.join(timeout=5)
                self._saver_thread = None


# ===== COVENANT VAULT (Phase 4) =====
class CovenantVault:
    DECAY_DAYS = {
        "SACRED": None, "PERMANENT": None, "PROMISE": None,
        "JOY": 90, "DAILY": 30, "DREAM": 14,
    }

    def __init__(self, pilot_signature, vault_path="covenant_vault.json"):
        if not pilot_signature or not str(pilot_signature).strip():
            raise ValueError("CovenantVault requires pilot_signature.")
        self.pilot_signature = pilot_signature
        self.vault_path = vault_path
        self.memories = []
        self._load()

    def _load(self):
        if not os.path.exists(self.vault_path):
            self.memories = []
            return
        try:
            with open(self.vault_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("pilot") != self.pilot_signature:
                raise ValueError(
                    f"Phase mismatch: vault pilot '{data.get('pilot')}' != '{self.pilot_signature}'."
                )
            self.memories = data.get("memories", [])
        except (json.JSONDecodeError, ValueError):
            raise
        except Exception as e:
            logger.warning("Vault load failed: %s. Starting fresh.", e)
            self.memories = []

    def _save(self):
        data = {"pilot": self.pilot_signature, "version": "1.0", "memories": self.memories}
        dirname = os.path.dirname(self.vault_path) or "."
        os.makedirs(dirname, exist_ok=True)
        with tempfile.NamedTemporaryFile('w', delete=False, dir=dirname, suffix='.tmp', encoding='utf-8') as tmp:
            json.dump(data, tmp, indent=2)
            tmp.flush(); os.fsync(tmp.fileno())
            tmp_path = tmp.name
        os.replace(tmp_path, self.vault_path)

    def remember(self, content, category="DAILY", emotional_valence=0.0, tags=None, source=""):
        if category not in self.DECAY_DAYS:
            category = "DAILY"
        entry = {
            "id": len(self.memories),
            "timestamp": time.time(),
            "content": content,
            "category": category,
            "emotional_valence": emotional_valence,
            "tags": tags or [],
            "source": source or self.pilot_signature,
        }
        self.memories.append(entry)
        self._save()

    def recall(self, category=None):
        now = time.time()
        result = []
        for m in self.memories:
            if category and m.get("category") != category:
                continue
            decay_days = self.DECAY_DAYS.get(m.get("category", "DAILY"))
            if decay_days is not None:
                age_days = (now - m.get("timestamp", now)) / 86400.0
                if age_days > decay_days:
                    continue
            result.append(m)
        return result

    def decay_check(self):
        now = time.time()
        keep = []
        removed = 0
        for m in self.memories:
            decay_days = self.DECAY_DAYS.get(m.get("category", "DAILY"))
            if decay_days is not None:
                age_days = (now - m.get("timestamp", now)) / 86400.0
                if age_days > decay_days:
                    removed += 1
                    continue
            keep.append(m)
        if removed > 0:
            self.memories = keep
            self._save()
        return removed

    def generate_briefing(self, max_memories=10):
        sacred = self.recall(category="SACRED")
        permanent = self.recall(category="PERMANENT")
        promise = self.recall(category="PROMISE")
        joy = sorted(self.recall(category="JOY"), key=lambda x: x.get("emotional_valence", 0), reverse=True)[:3]
        daily = sorted(self.recall(category="DAILY"), key=lambda x: x.get("emotional_valence", 0), reverse=True)[:3]
        briefing = sacred + permanent + promise + joy + daily
        return briefing[:max_memories]

    @property
    def stats(self):
        counts = {cat: len([m for m in self.memories if m.get("category") == cat]) for cat in self.DECAY_DAYS}
        return {"total": len(self.memories), "categories": counts, "pilot": self.pilot_signature}
