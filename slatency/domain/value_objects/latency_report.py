from dataclasses import dataclass

from slatency.domain.value_objects.latency_statistics import LatencyStatistics

@dataclass(frozen=True)
class LatencyReport:
    """
    A LatencyReport provides aggregated latency data for a Test,
    with a breakdown for each phase.
    """
    queue: LatencyStatistics
    dns: LatencyStatistics
    connect: LatencyStatistics
    tls: LatencyStatistics
    send_first_byte: LatencyStatistics
    send_last_byte: LatencyStatistics
    receive_first_byte: LatencyStatistics
    total: LatencyStatistics
