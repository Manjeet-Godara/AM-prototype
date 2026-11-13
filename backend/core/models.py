
from django.db import models


class System(models.Model):
    system_slug = models.CharField(max_length=100)
    environment = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["system_slug", "environment"],
                name="unique_system_environment"
            )
        ]

    def __str__(self):
        return f"{self.system_slug} - {self.environment}"


class Agent(models.Model):
    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name="agents"
    )
    agent_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["system", "agent_id"],
                name="unique_agent_per_system"
            )
        ]

    def __str__(self):
        return f"{self.agent_id} - {self.system}"


class Test(models.Model):
    system = models.ForeignKey(
        System,
        on_delete=models.CASCADE,
        related_name="tests"
    )
    test_id = models.CharField(max_length=255)
    test_name = models.CharField(max_length=255)
    service_tested = models.CharField(max_length=255)
    test_type = models.CharField(max_length=100)
    test_description = models.TextField(blank=True)

    registered_by = models.ForeignKey(
        Agent,
        on_delete=models.RESTRICT,
        related_name="registered_tests"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["system", "test_id"],
                name="unique_test_per_system"
            )
        ]

    def __str__(self):
        return f"{self.test_id} - {self.test_name}"


class TestRun(models.Model):
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="test_runs"
    )
    test_run_id = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["test", "test_run_id"],
                name="unique_test_run_per_test"
            )
        ]

    def __str__(self):
        return f"{self.test.test_id} - {self.test_run_id}"


class RunEvent(models.Model):
    run = models.ForeignKey(
        TestRun,
        on_delete=models.CASCADE,
        related_name="events"
    )
    sequence_number = models.PositiveIntegerField()
    event_type = models.CharField(max_length=100)

    occurred_at = models.DateTimeField()
    received_at = models.DateTimeField(auto_now_add=True)

    sent_by = models.ForeignKey(
        Agent,
        on_delete=models.RESTRICT,
        related_name="sent_events"
    )

    data = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["run", "sequence_number"],
                name="unique_sequence_per_run"
            )
        ]
        ordering = ["run", "sequence_number"]

    def __str__(self):
        return f"{self.run.test_run_id} - {self.sequence_number}"

