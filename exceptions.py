from typing import Optional, Tuple


class AutoClickerError(Exception):
    """Base exception class for all custom pyautogui-tools-15 operational anomalies."""

    def __init__(self, message: str, severity: str = "LOW") -> None:
        super().__init__(message)
        self.severity: str = severity.upper()

    def __str__(self) -> str:
        return f"[{self.severity}] {super().__str__()}"


class ScreenCoordOutOfBoundsError(AutoClickerError):
    """Raised when a target coordinates projection falls outside physical screen dimensions."""

    def __init__(
        self, 
        message: str, 
        attempted_coords: Tuple[int, int], 
        screen_resolution: Optional[Tuple[int, int]] = None
    ) -> None:
        super().__init__(message, severity="MEDIUM")
        self.attempted_coords: Tuple[int, int] = attempted_coords
        self.screen_resolution: Optional[Tuple[int, int]] = screen_resolution

    def radar_diagnostic(self) -> str:
        """Generates a creative telemetry readout illustrating where the miss occurred."""
        if not self.screen_resolution:
            return f"Out of bounds: {self.attempted_coords}. Screen limits undetected."

        sw, sh = self.screen_resolution
        ax, ay = self.attempted_coords
        
        horiz_dir = "LEFT" if ax < 0 else ("RIGHT" if ax >= sw else "OK")
        vert_dir = "ABOVE" if ay < 0 else ("BELOW" if ay >= sh else "OK")

        return (
            f"--- TELEMETRY MISALIGNMENT REPORT ---\n"
            f"Resolution Bound: {sw}x{sh} | Targeted Coordinates: ({ax}, {ay})\n"
            f"Directional Deviation: Horizontal={horiz_dir}, Vertical={vert_dir}\n"
            f"--------------------------------------"
        )


class SafetyLockoutError(AutoClickerError):
    """Raised when the fail-safe trigger threshold is breached to prevent desktop destruction."""

    def __init__(self, message: str = "Autoclicker failsafe activated. Safe zone breached!") -> None:
        super().__init__(message, severity="CRITICAL")
