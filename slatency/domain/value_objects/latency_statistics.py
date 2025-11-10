from dataclasses import dataclass

@dataclass(frozen=True)
class LatencyStatistics:
    """
    A LatencyStatistics object holds aggregated data for a single latency metric.
    """
    min: float
    max: float
    average: float
    p90: float
    p95: float
    p99: float
