class AutoclickerValidationError(ValueError):
    pass


def validate_coordinates(x: int, y: int) -> tuple[int, int]:
    if not isinstance(x, int) or not isinstance(y, int):
        raise AutoclickerValidationError("Coordinates must be integers")
    if x < 0 or y < 0:
        raise AutoclickerValidationError("Coordinates cannot be negative")
    return x, y


def validate_delay(delay: float) -> float:
    if not isinstance(delay, (int, float)):
        raise AutoclickerValidationError("Delay must be a numeric value")
    if delay < 0.001:
        raise AutoclickerValidationError("Delay must be at least 1ms to prevent system lock")
    return float(delay)


def validate_iterations(iterations: int) -> int:
    if not isinstance(iterations, int):
        raise AutoclickerValidationError("Iterations count must be an integer")
    if iterations < -1:
        raise AutoclickerValidationError("Iterations must be -1 for infinite or positive integer")
    return iterations


def sanity_check_config(config: dict) -> dict:
    x, y = validate_coordinates(config.get("x", 0), config.get("y", 0))
    delay = validate_delay(config.get("delay", 0.1))
    iterations = validate_iterations(config.get("iterations", 1))
    return {"x": x, "y": y, "delay": delay, "iterations": iterations}
