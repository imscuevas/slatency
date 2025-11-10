from typing import Protocol

from slatency.domain.entities.test import Test

class TestOutputPersistenceService(Protocol):
    """
    This service is responsible for saving the output of a test.
    It handles persisting the Test object, which includes the raw Response data.
    """
    def save(self, test: Test) -> None:
        """
        Saves the Test object to a persistent storage.
        """
        ...
