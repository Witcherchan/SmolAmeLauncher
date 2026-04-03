"""
Handles loading, saving, and validating the stats.json file.
"""

from json import load, dump
from datetime import datetime


class StatsManager:
    """Manages version and total play-time statistics."""

    def __init__(self, stats_path: str):
        self.stats_path = stats_path
        self.stats: dict = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def validate_and_load(self):
        """
        Validate stats.json on startup.
        Resets corrupt / missing fields and saves a clean copy.
        Raises SystemExit if something goes fatally wrong.
        """
        print("--- Started validating stats ---")

        # Load (or reset) the file
        try:
            with open(self.stats_path, "r") as f:
                self.stats = load(f)
            print("Stats.json loaded successfully!")
        except Exception:
            self.stats = {}
            print("Stats.json invalid or missing – starting fresh.")

        # Validate total_play_time
        if "total_play_time" not in self.stats:
            self.stats["total_play_time"] = 0
            print("Created total_play_time.")
        elif not isinstance(self.stats["total_play_time"], (int, float)):
            self.stats["total_play_time"] = 0
            print("Reset invalid total_play_time to 0.")
        else:
            print("total_play_time OK.")

        # Validate version_play_time
        if "version_play_time" not in self.stats:
            self.stats["version_play_time"] = {}
            print("Created version_play_time.")
        elif not isinstance(self.stats["version_play_time"], dict):
            self.stats["version_play_time"] = {}
            print("Reset invalid version_play_time to {}.")
        else:
            print("version_play_time OK.")

        self.save()
        print("--- Finished validating stats ---")

    def ensure_version_entry(self, version_name: str):
        """Create a default stats entry for version_name if it doesn't exist."""
        if version_name not in self.stats["version_play_time"]:
            print(f"Creating new stat entry for: {version_name}")
            self.stats["version_play_time"][version_name] = {
                "last_played": "Not played",
                "time_played": 0,
            }
        else:
            print(f"Stat entry already exists for: {version_name}")

    def record_session(self, version_name: str, seconds_played: float):
        """Add seconds_played to both the version and total counters."""
        vpt = self.stats["version_play_time"][version_name]
        vpt["time_played"] = round(vpt["time_played"] + seconds_played, 0)
        self.stats["total_play_time"] = round(
            self.stats["total_play_time"] + seconds_played, 0
        )

    def record_last_played(self, version_name: str):
        """Stamp the current datetime as last_played for version_name."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.stats["version_play_time"][version_name]["last_played"] = date

    def save(self):
        """Write current stats to disk."""
        with open(self.stats_path, "w") as f:
            dump(self.stats, f, indent=4)
        print("Stats saved.")

    # ------------------------------------------------------------------
    # Convenience accessors
    # ------------------------------------------------------------------

    @property
    def total_play_time(self) -> float:
        return self.stats.get("total_play_time", 0)

    def version_last_played(self, version_name: str) -> str:
        return self.stats["version_play_time"][version_name]["last_played"]

    def version_time_played(self, version_name: str) -> float:
        return self.stats["version_play_time"][version_name]["time_played"]
