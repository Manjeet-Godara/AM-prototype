import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from .models import System, Agent


import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db import transaction

from .models import System, Agent, Test

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

