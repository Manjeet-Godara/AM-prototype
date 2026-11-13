import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction, IntegrityError
from django.views.decorators.csrf import csrf_exempt
from .models import System, Agent


import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction
from django.utils.dateparse import parse_datetime
from .models import System, Agent, Test, TestRun, RunEvent

@csrf_exempt
@require_POST
def register_agent(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    system_slug = data.get("system_slug")
    environment = data.get("environment")
    agent_id = data.get("agent_id")

    # 1. Validate fields
    if not all(
        isinstance(value, str) and value.strip()
        for value in [system_slug, environment, agent_id]
    ):
        return JsonResponse({
            "error": "system_slug, environment and agent_id are required"
        }, status=400)

    # 2. Find or create System and Agent
    with transaction.atomic():

        system, system_created = System.objects.get_or_create(
            system_slug=system_slug,
            environment=environment
        )

        agent, agent_created = Agent.objects.get_or_create(
            system=system,
            agent_id=agent_id
        )

        # 3. Update last_seen_at on both
        now = timezone.now()

        System.objects.filter(pk=system.pk).update(last_seen_at=now)
        Agent.objects.filter(pk=agent.pk).update(last_seen_at=now)

    # 4. Return response
    return JsonResponse({
        "message": "Agent registration processed successfully",
        "system": {
            "id": system.id,
            "system_slug": system.system_slug,
            "environment": system.environment,
            "status": "created" if system_created else "already existed"
        },
        "agent": {
            "id": agent.id,
            "agent_id": agent.agent_id,
            "status": "created" if agent_created else "already existed"
        }
    }, status=201)


def get_registered_agent(system_slug, environment, agent_id):

    system = System.objects.filter(
        system_slug=system_slug,
        environment=environment
    ).first()

    if not system:
        return None, None

    agent = Agent.objects.filter(
        system=system,
        agent_id=agent_id
    ).first()

    if not agent:
        return None, None

    return system, agent

@csrf_exempt
@require_POST
def register_test(request):

    # Parse incoming JSON
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "status": "invalid_request",
            "message": "Invalid JSON payload"
        }, status=400)

    # Extract identification details
    system_slug = data.get("system_slug")
    environment = data.get("environment")
    agent_id = data.get("agent_id")

    # Verify System and Agent
    system, agent = get_registered_agent(
        system_slug,
        environment,
        agent_id
    )

    if not system or not agent:
        return JsonResponse({
            "status": "unauthorized",
            "message": "Agent is not registered"
        }, status=401)

    # Extract test details
    test_id = data.get("test_id")

    # Check if Test already exists in this System
    existing_test = Test.objects.filter(
        system=system,
        test_id=test_id
    ).exists()

    if existing_test:
        return JsonResponse({
            "status": "already_exists",
            "message": "Test already exists in this System",
            "test_id": test_id
        }, status=409)

    # Register Test
    test = Test.objects.create(
        system=system,
        registered_by=agent,
        test_id=test_id,
        test_name=data.get("test_name"),
        service_tested=data.get("service_tested"),
        test_type=data.get("test_type"),
        test_description=data.get("test_description", "")
    )

    return JsonResponse({
        "status": "created",
        "message": "Test registered successfully",
        "test_id": test.test_id
    }, status=201)


def validate_event(sequence_number, event_type, occurred_at):

    # 1. Allowed sequence number and event type mapping
    allowed_events = {
        1: ["test.queued"],
        2: ["test.started"],
        3: ["test.passed", "test.failed", "test.errored"],
        4: ["cleanup.started"],
        5: ["cleanup.completed"],
        6: ["test.completed"]
    }

    # 2. Check sequence number and event type
    if sequence_number not in allowed_events:
        return False

    if event_type not in allowed_events[sequence_number]:
        return False

    # 3. Check occurred_at timestamp
    if not isinstance(occurred_at, str):
        return False

    if parse_datetime(occurred_at) is None:
        return False

    return True

def verify_event_sender(system_slug, environment, agent_id, test_id):

    # Step 1: Verify System and Agent
    system, agent = get_registered_agent(
        system_slug,
        environment,
        agent_id
    )

    if not system or not agent:
        return None

    # Step 2: Verify that the Test belongs to this System
    test_exists = Test.objects.filter(
        system=system,
        test_id=test_id
    ).exists()

    if not test_exists:
        return None

    # All checks passed
    return agent


def get_or_create_test_run(system, test_id, test_run_id):

    # Step 1: Find the Test in the given System
    test = Test.objects.filter(
        system=system,
        test_id=test_id
    ).first()

    if not test:
        return None

    # Step 2: Find existing TestRun or create a new one
    test_run, created = TestRun.objects.get_or_create(
        test=test,
        test_run_id=test_run_id
    )

    # Step 3: Return TestRun object
    return test_run


@csrf_exempt
@require_POST
def receive_event(request):

    # 1. Parse incoming JSON
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            "status": "invalid_request",
            "message": "Invalid JSON payload"
        }, status=400)

    # 2. Extract common fields
    system_slug = data.get("system_slug")
    environment = data.get("environment")
    agent_id = data.get("agent_id")
    test_id = data.get("test_id")
    test_run_id = data.get("test_run_id")

    sequence_number = data.get("sequence_number")
    event_type = data.get("event_type")
    occurred_at = data.get("occurred_at")

    # 3. Verify Agent and Test authorization
    agent = verify_event_sender(
        system_slug,
        environment,
        agent_id,
        test_id
    )

    if agent is None:
        return JsonResponse({
            "status": "unauthorized",
            "message": "Agent or Test is not registered"
        }, status=401)

    # 4. Validate event details
    if not validate_event(
        sequence_number,
        event_type,
        occurred_at
    ):
        return JsonResponse({
            "status": "invalid_request",
            "message": "Invalid event details"
        }, status=400)

    # 5. Get System
    system = System.objects.get(
        system_slug=system_slug,
        environment=environment
    )

    # 6. Get existing TestRun or create a new one
    test_run = get_or_create_test_run(
        system,
        test_id,
        test_run_id
    )

    if test_run is None:
        return JsonResponse({
            "status": "unauthorized",
            "message": "Test is not registered"
        }, status=401)

    # 7. Prepare event data
    event_data = {}

    if sequence_number == 3:
        event_data = {
            "summary": data.get("summary"),
            "expected": data.get("expected"),
            "actual": data.get("actual"),
            "suggested_fix": data.get("suggested_fix")
        }

    # 8. Check and create event
    try:
        with transaction.atomic():

            existing_event = RunEvent.objects.filter(
                run=test_run,
                sequence_number=sequence_number
            ).exists()

            if existing_event:
                return JsonResponse({
                    "status": "already_exists",
                    "message": "Event already exists",
                    "test_run_id": test_run.test_run_id,
                    "sequence_number": sequence_number
                }, status=409)

            event = RunEvent.objects.create(
                run=test_run,
                sequence_number=sequence_number,
                event_type=event_type,
                occurred_at=parse_datetime(occurred_at),
                sent_by=agent,
                data=event_data
            )

    except IntegrityError:
        return JsonResponse({
            "status": "already_exists",
            "message": "Event already exists"
        }, status=409)

    now = timezone.now()

    system.last_seen_at = now
    system.save(update_fields=["last_seen_at"])

    agent.last_seen_at = now
    agent.save(update_fields=["last_seen_at"])
    # 9. Return successful response
    return JsonResponse({
        "status": "created",
        "message": "Event registered successfully",
        "test_run_id": test_run.test_run_id,
        "sequence_number": event.sequence_number
    }, status=201)

from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .models import System, TestRun, RunEvent

@csrf_exempt
@require_GET
def get_systems(request):

    systems = System.objects.all().order_by("id")

    response_data = []

    for system in systems:

        # Get all agent IDs belonging to this system
        agent_ids = list(
            system.agents.values_list("agent_id", flat=True)
        )

        # Count registered tests
        test_count = system.tests.count()

        # Find the latest TestRun across all tests of this system
        latest_run = TestRun.objects.filter(
            test__system=system
        ).order_by("-created_at").first()

        latest_outcome = None

        if latest_run:

            # Find the outcome event of the latest run
            outcome_event = RunEvent.objects.filter(
                run=latest_run,
                sequence_number=3
            ).first()

            if outcome_event:
                latest_outcome = outcome_event.event_type

        # Prepare system response
        response_data.append({
            "id": system.id,
            "system_slug": system.system_slug,
            "environment": system.environment,
            "agent_ids": agent_ids,
            "test_count": test_count,
            "last_seen_at": system.last_seen_at,
            "latest_run_outcome": latest_outcome
        })

    return JsonResponse({
        "status": "success",
        "systems": response_data
    }, status=200)