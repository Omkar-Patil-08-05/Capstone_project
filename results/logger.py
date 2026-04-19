import csv
import os
import time

class ResultLogger:

    def __init__(self):
        base_path = os.path.expanduser("~/capstone_project/results")
        os.makedirs(base_path, exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")

        self.coverage_file = open(f"{base_path}/coverage_{timestamp}.csv", "w", newline="")
        self.position_file = open(f"{base_path}/positions_{timestamp}.csv", "w", newline="")

        self.coverage_writer = csv.writer(self.coverage_file)
        self.position_writer = csv.writer(self.position_file)

        # headers
        self.coverage_writer.writerow(["time_step", "coverage"])
        self.position_writer.writerow(["time_step", "drone", "x", "y"])

        self.step = 0

    def log(self, coverage, positions):

        # coverage
        self.coverage_writer.writerow([self.step, coverage])

        # positions
        for i, pos in enumerate(positions):
            self.position_writer.writerow([self.step, f"drone{i+1}", pos[0], pos[1]])

        # ✅ FORCE WRITE TO DISK
        self.coverage_file.flush()
        self.position_file.flush()

        self.step += 1

    def close(self):
        self.coverage_file.close()
        self.position_file.close()