from typing import Protocol

from slatency.domain.entities.test import Test

class TestRunnerService(Protocol):
    """
    This service is responsible for executing a Test.
    It takes a Test object, sends the defined HTTP requests,
    and records the Response objects.
    """
    def execute(self, test: Test) -> Test:
        """
        Executes the test based on its `expected_responses` attribute.
        """
        ...
