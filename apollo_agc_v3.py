"""
Apollo 11 Guidance Computer Simulation (Visual Dashboard Version)
Inspired by Margaret Hamilton's real-time fault-tolerant executive design (1969)
"""

import time
import random
import os

class AGCSystem:
    def __init__(self):
        self.tasks = {
            "landing_guidance": {"priority": 1, "active": True},
            "radar_tracking": {"priority": 2, "active": True},
            "telemetry": {"priority": 3, "active": True},
            "camera_recording": {"priority": 4, "active": True}
        }
        self.error_flag = False
        self.overload_count = 0
        self.cycle = 0

    def clear_console(self):
        # Works for macOS, Linux, Windows
        os.system('cls' if os.name == 'nt' else 'clear')

    def simulate_sensor_load(self):
        return random.choice([0.6, 0.8, 1.0, 1.2, 1.5, 2.0])

    def check_system_load(self):
        load = self.simulate_sensor_load()
        if load > 1.0:
            self.error_flag = True
            self.overload_count += 1
        else:
            self.error_flag = False
            if self.overload_count > 0:
                self.overload_count -= 1
        return load

    def recover_and_prioritize(self):
        if not self.error_flag:
            if self.overload_count == 0:
                self.resume_tasks()
            return "STABLE"

        for name, task in sorted(self.tasks.items(), key=lambda t: t[1]["priority"]):
            if task["priority"] > 2:
                task["active"] = False
            else:
                task["active"] = True
        return "OVERLOAD"

    def resume_tasks(self):
        for task in self.tasks.values():
            task["active"] = True

    def render_dashboard(self, load, state):
        self.clear_console()
        self.cycle += 1

        # CPU load bar
        bar_length = int(min(load, 2.0) * 20)
        bar = "█" * bar_length + "-" * (40 - bar_length)

        print(f"\n🛰️  Apollo Guidance Computer — Real-Time Simulation")
        print(f"----------------------------------------------")
        print(f"Cycle: {self.cycle}")
        print(f"CPU Load: [{bar}] {load:.2f}x")
        print(f"System State: {'⚠️  OVERLOAD' if state == 'OVERLOAD' else '✅ STABLE'}\n")

        # Task table
        print(f"{'Task':<20} | {'Priority':<8} | {'Status'}")
        print("-" * 45)
        for name, info in self.tasks.items():
            status = "🟢 ACTIVE" if info["active"] else "🔴 SUSPENDED"
            print(f"{name:<20} | {info['priority']:<8} | {status}")
        print("\n")

    def run_cycle(self, cycles=15):
        for _ in range(cycles):
            load = self.check_system_load()
            state = self.recover_and_prioritize()
            self.render_dashboard(load, state)
            time.sleep(1)

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if __name__ == "__main__":
    agc = AGCSystem()
    agc.run_cycle()
    print("✅ Mission complete. All systems nominal.")

