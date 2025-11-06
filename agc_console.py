"""
Apollo 11 Guidance Computer — Mission Console (Tkinter GUI)
Reimagines Margaret Hamilton's fault-tolerant executive: prioritization, overload handling, self-healing.
No external dependencies. Run with: python3 agc_console.py
"""

import tkinter as tk
import random
import time

class AGCSystem:
    def __init__(self):
        # lower priority number = more critical
        self.tasks = {
            "landing_guidance": {"priority": 1, "active": True, "blink": False},
            "radar_tracking":   {"priority": 2, "active": True, "blink": False},
            "telemetry":        {"priority": 3, "active": True, "blink": False},
            "camera_recording": {"priority": 4, "active": True, "blink": False}
        }
        self.error_flag = False
        self.overload_count = 0
        self.cycle = 0
        self.running = False

    def simulate_sensor_load(self):
        # Random load spikes emulate radar + guidance contention
        return random.choice([0.6, 0.8, 1.0, 1.2, 1.5, 1.8, 2.0])

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
        # Overload: preserve critical tasks, suspend non-critical
        if self.error_flag:
            for name, task in sorted(self.tasks.items(), key=lambda t: t[1]["priority"]):
                task["active"] = task["priority"] <= 2
                # blink non-critical when suspended to draw attention
                task["blink"] = not task["active"]
            return "OVERLOAD"
        # Stable: if cool-down complete, resume all tasks
        if self.overload_count == 0:
            for task in self.tasks.values():
                task["active"] = True
                task["blink"]  = False
            return "STABLE"
        # Still cooling down (recent overload) but not currently overloaded
        return "COOLDOWN"

class AGCMissionConsole(tk.Tk):
    def __init__(self, agc: AGCSystem, refresh_ms=800):
        super().__init__()
        self.title("Apollo Guidance Computer — Mission Console")
        self.geometry("760x520")
        self.configure(bg="#0b1221")  # deep space
        self.agc = agc
        self.refresh_ms = refresh_ms
        self.last_blink_state = False
        self._build_ui()
        self._update_ui(initial=True)

    def _build_ui(self):
        # Header
        header = tk.Label(self, text="APOLLO GUIDANCE COMPUTER — REAL-TIME CONSOLE",
                          font=("SF Pro Display", 16, "bold"), fg="#d6e4ff", bg="#0b1221")
        header.pack(pady=10)

        # Status frame (cycle, state)
        self.status_frame = tk.Frame(self, bg="#0b1221")
        self.status_frame.pack(pady=4)

        self.cycle_var = tk.StringVar(value="Cycle: 0")
        self.state_var = tk.StringVar(value="State: INIT")
        self.alert_var = tk.StringVar(value="")

        tk.Label(self.status_frame, textvariable=self.cycle_var, font=("Consolas", 12),
                 fg="#c7d2fe", bg="#0b1221").grid(row=0, column=0, padx=12)
        tk.Label(self.status_frame, textvariable=self.state_var, font=("Consolas", 12, "bold"),
                 fg="#a7f3d0", bg="#0b1221").grid(row=0, column=1, padx=12)
        tk.Label(self.status_frame, textvariable=self.alert_var, font=("Consolas", 12, "bold"),
                 fg="#fca5a5", bg="#0b1221").grid(row=0, column=2, padx=12)

        # Load meter
        lm_frame = tk.Frame(self, bg="#0b1221")
        lm_frame.pack(pady=8)
        tk.Label(lm_frame, text="CPU LOAD", font=("Consolas", 12, "bold"),
                 fg="#fde68a", bg="#0b1221").pack(anchor="w")

        self.canvas = tk.Canvas(lm_frame, width=700, height=36, bg="#0b1221", highlightthickness=0)
        self.canvas.pack()
        # background bar
        self.canvas.create_rectangle(10, 10, 710, 30, fill="#1f2937", outline="#374151")
        # dynamic bar
        self.load_rect = self.canvas.create_rectangle(10, 10, 10, 30, fill="#60a5fa", outline="")
        # tick marks (1.0x and 2.0x)
        self.canvas.create_line(360, 8, 360, 32, fill="#6b7280")  # ~1.0x mark
        self.canvas.create_line(710, 8, 710, 32, fill="#6b7280")  # 2.0x end

        # Task table
        table_frame = tk.Frame(self, bg="#0b1221")
        table_frame.pack(pady=8, fill="x", padx=16)

        headers = ["Task", "Priority", "Status"]
        widths = [26, 10, 20]
        for i, (h, w) in enumerate(zip(headers, widths)):
            tk.Label(table_frame, text=h, width=w, anchor="w", font=("Consolas", 12, "bold"),
                     fg="#93c5fd", bg="#0b1221").grid(row=0, column=i, padx=6)

        self.task_rows = {}
        for r, (name, info) in enumerate(self.agc.tasks.items(), start=1):
            lbl_name = tk.Label(table_frame, text=name, width=widths[0], anchor="w",
                                font=("Consolas", 12), fg="#e5e7eb", bg="#0b1221")
            lbl_prio = tk.Label(table_frame, text=str(info["priority"]), width=widths[1], anchor="w",
                                font=("Consolas", 12), fg="#e5e7eb", bg="#0b1221")
            lbl_stat = tk.Label(table_frame, text="", width=widths[2], anchor="w",
                                font=("Consolas", 12, "bold"), fg="#10b981", bg="#0b1221")
            lbl_name.grid(row=r, column=0, padx=6, pady=2, sticky="w")
            lbl_prio.grid(row=r, column=1, padx=6, pady=2, sticky="w")
            lbl_stat.grid(row=r, column=2, padx=6, pady=2, sticky="w")
            self.task_rows[name] = {"name": lbl_name, "prio": lbl_prio, "stat": lbl_stat}

        # Controls
        ctrl = tk.Frame(self, bg="#0b1221")
        ctrl.pack(pady=12)
        self.btn_start = tk.Button(ctrl, text="Start", width=10, command=self.start, bg="#111827", fg="#e5e7eb")
        self.btn_stop  = tk.Button(ctrl, text="Stop",  width=10, command=self.stop,  bg="#111827", fg="#e5e7eb")
        self.btn_start.grid(row=0, column=0, padx=6)
        self.btn_stop.grid(row=0, column=1, padx=6)

        # Footer
        tk.Label(self, text="Hamilton Executive Model: prioritize → degrade gracefully → self-heal",
                 font=("Consolas", 10), fg="#9ca3af", bg="#0b1221").pack(pady=6)

    def start(self):
        if not self.agc.running:
            self.agc.running = True
            self._tick()

    def stop(self):
        self.agc.running = False

    def _tick(self):
        if not self.agc.running:
            return
        self._update_logic()
        self._update_ui()
        self.after(self.refresh_ms, self._tick)

    def _update_logic(self):
        self.agc.cycle += 1
        self.load = self.agc.check_system_load()
        self.state = self.agc.recover_and_prioritize()

    def _update_ui(self, initial=False):
        # Cycle & state
        self.cycle_var.set(f"Cycle: {self.agc.cycle}")
        state_text = {"OVERLOAD": "⚠ OVERLOAD", "COOLDOWN": "… COOL-DOWN", "STABLE": "✅ STABLE"}.get(self.state, self.state)
        self.state_var.set(f"State: {state_text}")
        self.alert_var.set("1201/1202-like Executive Overflow" if self.state == "OVERLOAD" else "")

        # Load bar (map 0.0–2.0x to 10–710 px)
        clamped = max(0.0, min(self.load, 2.0))
        x = 10 + int(clamped * (700 / 2.0))
        color = "#34d399" if clamped <= 1.0 else "#f59e0b" if clamped <= 1.5 else "#ef4444"
        self.canvas.itemconfig(self.load_rect, fill=color)
        self.canvas.coords(self.load_rect, 10, 10, x, 30)

        # Blink state toggles each refresh
        self.last_blink_state = not self.last_blink_state

        # Update tasks rows
        for name, info in self.agc.tasks.items():
            lbl = self.task_rows[name]["stat"]
            if info["active"]:
                lbl.config(text="ACTIVE", fg="#10b981")  # green
            else:
                # blinking red/yellow to draw attention when suspended
                blink_fg = "#f87171" if self.last_blink_state else "#fbbf24"
                lbl.config(text="SUSPENDED", fg=blink_fg)

        # Optional first paint adjustment
        if initial:
            self.update_idletasks()

def main():
    agc = AGCSystem()
    app = AGCMissionConsole(agc, refresh_ms=700)
    # Autostart for convenience
    app.start()
    app.mainloop()

if __name__ == "__main__":
    main()

