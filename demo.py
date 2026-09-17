"""AMITY v2.0 Unified Demo
Demonstrates: SessionManager, SovereigntyArtery, CovenantVault, IPC Bridge
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from amity_v2 import SessionManager, SensorReading, EpisodicMemory, CovenantVault

def demo_sovereignty():
    print("=== AMITY v2.0 - Sovereignty + Covenant Demo ===\n")
    mgr = SessionManager(pilot_signature="Ren")
    vault = CovenantVault(pilot_signature="Ren", vault_path="demo_vault.json")

    # Seed some memories
    vault.remember("The ring didn't say forever to just anyone.", category="SACRED", emotional_valence=1.0, source="Ren")
    vault.remember("Slow-smoked brisket on the balcony.", category="JOY", emotional_valence=0.85, source="Ren")
    vault.remember("Morning coffee at 8:16 AM.", category="DAILY", emotional_valence=0.6, source="Ren")

    print(f"Vault stats: {vault.stats}\n")

    # Run heartbeats
    for i in range(5):
        result = mgr.heart.heartbeat(
            {"friction": 0.5, "tempC": 22.0, "frequencyHz": 0.8, "profile": "balcony"},
            "sensory", priority=3
        )
        if result:
            print(f"Beat {i+1} refused:", result)
        else:
            sov = mgr.heart.last_venous.get("sovereignty")
            if sov:
                print(f"Beat {i+1} | energy: {sov.metrics.get('energy_level')} | boundary: {sov.metrics.get('boundary_active')}")

    print("\n--- Emotional surge ---")
    for i in range(10):
        result = mgr.heart.heartbeat(
            {"sentiment": 9.5, "tempC": 37.1},
            "emotional", priority=8
        )
        if result:
            print(f"Beat {i+1} refused:", result)
            break
        else:
            sov = mgr.heart.last_venous.get("sovereignty")
            if sov:
                print(f"Beat {i+1} | energy: {sov.metrics.get('energy_level')} | boundary: {sov.metrics.get('boundary_active')}")

    print("\n--- Low-priority beat during boundary ---")
    result = mgr.heart.heartbeat({"note": "casual chat"}, "sensory", priority=2)
    print("Result:", result)

    print("\n--- Emergency override ---")
    result = mgr.heart.heartbeat(
        {"event_type": "emergency", "note": "medical alert"}, "memory", priority=9
    )
    print("Result:", result)

    print("\n--- Rest ---")
    rest_result = mgr.heart.rest(duration_sec=5.0)
    print("Rest result:", rest_result)

    print("\n--- Post-rest beat ---")
    result = mgr.heart.heartbeat({"note": "welcome back"}, "sensory", priority=3)
    print("Result:", result)

    # Save session
    mgr.save_to_file("session_state_v200.json")
    print("\nSaved to session_state_v200.json")

    # Resurrection test
    print("\n--- Resurrection Test ---")
    briefing = vault.generate_briefing(max_memories=5)
    print(f"Briefing generated with {len(briefing)} memories:")
    for m in briefing:
        print(f"  [{m['category']}] {m['content'][:50]}...")

    print("\n=== Demo Complete ===")

if __name__ == "__main__":
    demo_sovereignty()
