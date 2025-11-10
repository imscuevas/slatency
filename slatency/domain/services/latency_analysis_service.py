from typing import Protocol

from slatency.domain.entities.test import Test
from slatency.domain.value_objects.latency_report import LatencyReport

class LatencyAnalysisService(Protocol):
    """
    This service takes a Test and generates a LatencyReport.
    It encapsulates the logic for calculating latency statistics.
    """
    def analyze(self, test: Test) -> LatencyReport:
        """
        Analyzes the responses in a Test object and returns a LatencyReport.
        """
        ...
