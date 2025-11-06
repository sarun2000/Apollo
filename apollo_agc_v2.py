"""
Apollo 11 Guidance Computer Simulation (Self-Healing Version)
Inspired by Margaret Hamilton's fault-tolerant executive design (1969)
"""

import time
import random

class AGCSystem:
    def __init__(self):
        # Each task has a priority (lower = more critical)
        self.tasks = {
            "landing_guidance": {"priority": 1, "active": True},
            "radar_tracking": {"priority": 2, "active": True},
            "telemetry": {"priority": 3, "active": True},
            "camera_recording": {"priority": 4, "active": True}
        }
        self.error_flag = False
        self.overload_count = 0

    def simulate_sensor_load(self):
        # Random system load spikes (simulating radar interference)
        return random.choice([0.6, 0.8, 1.0, 1.3, 1.6, 2.0])

    def check_system_load(self):
        load = self.simulate_sensor_load()
        print(f"[SYSTEM] Current CPU load: {load:.1f}x")

        if load > 1.0:
            self.error_flag = True
            self.overload_count += 1
            print(f"[ALERT] Executive Overflow detected! (count={self.overload_count})")
        else:
            self.error_flag = False
            if self.overload_count > 0:
                self.overload_count -= 1  # Gradual cooldown
        return load

    def recover_and_prioritize(self):
        if not self.error_flag:
            # If system stable for long enough, resume suspended tasks
            if self.overload_count == 0:
                self.resume_tasks()
            print("[STATUS] System stable. Continuing normal operations.\n")
            return

        print("[RECOVERY] Overload detected — reallocating CPU resources...")
        for name, task in sorted(self.tasks.items(), key=lambda t: t[1]["priority"]):
            if task["priority"] > 2:
                if task["active"]:
                    task["active"] = False
                    print(f"  • Suspended: {name}")
            else:
                print(f"  • Preserved: {name}")
        print("[RECOVERY] Critical operations remain online.\n")

    def resume_tasks(self):
        print("[RESUME] System stabilized — restoring suspended tasks...")
        for name, task in self.tasks.items():
            if not task["active"]:
                task["active"] = True
                print(f"  • Resumed: {name}")
        print("[RESUME] All systems nominal again.\n")

    def run_cycle(self, cycles=8):
        for i in range(cycles):
            print(f"--- CYCLE {i+1} ---")
            self.check_system_load()
            self.recover_and_prioritize()
            time.sleep(1)

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    print("🛰️  Apollo Guidance Computer — Self-Healing Simulation Start\n")
    agc = AGCSystem()
    agc.run_cycle()
    print("✅  Simulation complete. Mission stable.")

