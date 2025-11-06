#!/usr/bin/env python3
"""
Multi-Agent Customer Support Triage System - CLI Runner

This script runs the complete workflow from the command line without needing Jupyter.
"""

import os
import sys
import json
from dotenv import load_dotenv
from conductor.client.configuration.configuration import Configuration
from conductor.shared.configuration.settings.authentication_settings import AuthenticationSettings
from conductor.client.orkes_clients import OrkesClients
from conductor.client.http.models import Task, WorkflowDef, TaskDef
from conductor.client.worker.worker_task import WorkerTask
from conductor.client.workflow.conductor_workflow import ConductorWorkflow
from conductor.client.workflow.task.llm_tasks.llm_chat_complete import LlmChatComplete, ChatMessage
from conductor.client.workflow.task.simple_task import SimpleTask
from conductor.client.workflow.executor.workflow_executor import WorkflowExecutor
from conductor.client.automator.task_handler import TaskHandler


def load_configuration():
    """Load environment variables and configure Orkes client"""
    load_dotenv()

    key_id = os.getenv("ORKES_KEY_ID")
    key_secret = os.getenv("ORKES_KEY_SECRET")
    server_url = os.getenv("ORKES_SERVER_URL", "https://play.orkes.io/api")

    if not key_id or not key_secret:
        print("❌ Error: ORKES_KEY_ID and ORKES_KEY_SECRET must be set in .env file")
        print("   Copy .env.example to .env and add your credentials")
        sys.exit(1)

    auth_settings = AuthenticationSettings(
        key_id=key_id,
        key_secret=key_secret
    )

    config = Configuration(
        server_api_url=server_url,
        authentication_settings=auth_settings
    )

    return config


def create_classifier_agent():
    """Creates the classifier agent task"""

    return LlmChatComplete(
        task_ref_name="classify_ticket",
        llm_provider="nl-openai",
        model="gpt-4",  # Using GPT-4
        messages=[
            ChatMessage(role="system", message="You are a customer support ticket classifier. Analyze tickets and provide category (billing/technical/account/general), sentiment (positive/neutral/negative/angry), and urgency (low/medium/high/critical) in JSON format with a reasoning field."),
            ChatMessage(role="user", message="${workflow.input.ticket_content}")
        ]
    )


def create_knowledge_agent():
    """Creates the knowledge search agent"""

    return LlmChatComplete(
        task_ref_name="search_knowledge",
        llm_provider="nl-openai",
        model="gpt-4",  # Using GPT-4
        messages=[
            ChatMessage(role="system", message="You are a knowledge base expert. Provide KB articles, resolution steps, confidence level (0-100), and a suggested customer response in JSON format."),
            ChatMessage(role="user", message="Ticket: ${workflow.input.ticket_content}. Category: ${classify_ticket.output.result.category}. Urgency: ${classify_ticket.output.result.urgency}")
        ]
    )


@WorkerTask(task_definition_name='send_escalation_notification', domain='support', poll_interval=0.5)
def send_notification(task_input):
    """Custom worker that sends notifications when tickets are escalated"""
    ticket_id = task_input.get('ticket_id')
    urgency = task_input.get('urgency')
    category = task_input.get('category')
    assigned_to = task_input.get('assigned_to', 'support-team')

    print(f"🚨 Escalating ticket {ticket_id}")
    print(f"   Category: {category}")
    print(f"   Urgency: {urgency}")
    print(f"   Assigned to: {assigned_to}")

    notification_channels = []
    if urgency in ['critical', 'high']:
        notification_channels.extend(['slack', 'email', 'pagerduty'])
    else:
        notification_channels.append('email')

    return {
        'notification_sent': True,
        'channels': notification_channels,
        'timestamp': '2025-01-15T10:30:00Z',
        'assigned_team': assigned_to
    }


def create_escalation_decision():
    """Creates escalation decision tasks"""
    escalation_eval = SimpleTask(
        task_def_name="evaluate_escalation",
        task_reference_name="eval_escalation"
    )

    notification_task = SimpleTask(
        task_def_name="send_escalation_notification",
        task_reference_name="notify_team"
    )

    # Set input parameters after creating the task
    notification_task.input_parameters = {
        'ticket_id': '${workflow.input.ticket_id}',
        'urgency': '${classify_ticket.output.result.urgency}',
        'category': '${classify_ticket.output.result.category}',
        'assigned_to': '${eval_escalation.output.assigned_team}'
    }

    return escalation_eval, notification_task


def create_support_triage_workflow(workflow_executor):
    """Creates the complete multi-agent support triage workflow"""
    workflow = ConductorWorkflow(
        name="customer_support_triage",
        version=1,
        executor=workflow_executor
    )

    # Add all tasks in sequence
    classifier = create_classifier_agent()
    knowledge = create_knowledge_agent()
    # Skip escalation for now - testing core LLM agents first
    # escalation_eval, notification = create_escalation_decision()

    # Build the workflow chain
    workflow >> classifier >> knowledge
    # workflow >> escalation_eval >> notification

    return workflow


def monitor_workflow(clients, workflow_id):
    """Monitor and display workflow execution status"""
    workflow_client = clients.get_workflow_client()
    execution = workflow_client.get_workflow(workflow_id, include_tasks=True)

    print(f"\n{'='*70}")
    print(f"Workflow Status: {execution.status}")
    print(f"{'='*70}")

    for task in execution.tasks:
        print(f"\n📋 {task.task_type}: {task.reference_task_name}")
        print(f"   Status: {task.status}")
        if task.output_data:
            output_preview = json.dumps(task.output_data, indent=2)[:300]
            print(f"   Output: {output_preview}...")

    return execution


def main():
    """Main execution function"""
    print("🚀 Multi-Agent Customer Support Triage System")
    print("=" * 70)

    # Load configuration
    print("\n📋 Loading configuration...")
    config = load_configuration()
    print(f"✅ Connected to: {config.host}")

    # Initialize clients
    clients = OrkesClients(config)
    workflow_executor = WorkflowExecutor(config)

    # Create workflow
    print("\n🔧 Creating workflow...")
    support_workflow = create_support_triage_workflow(workflow_executor)
    print("✅ Workflow created: customer_support_triage")

    # Register worker (optional - needed for notifications)
    # Note: Worker registration has some compatibility issues with current SDK version
    # The workflow will still run, but custom worker tasks will need to be run separately
    print("\n👷 Skipping worker registration for this test...")
    print("   (Worker tasks can be run separately in production)")

    # Sample test tickets
    test_tickets = [
        {
            "ticket_id": "TKT-001",
            "ticket_content": "I can't log into my account. I've tried resetting my password but I'm not receiving the email."
        },
        {
            "ticket_id": "TKT-002",
            "ticket_content": "URGENT: Our production system is down and we're losing money every minute. This is critical!"
        },
        {
            "ticket_id": "TKT-003",
            "ticket_content": "Hi, I was charged twice for my subscription this month. Can you help?"
        }
    ]

    # Execute workflows
    print(f"\n🎫 Processing {len(test_tickets)} tickets...\n")

    workflow_ids = []
    for ticket in test_tickets:
        print(f"\n{'='*70}")
        print(f"Processing: {ticket['ticket_id']}")
        print(f"Content: {ticket['ticket_content'][:60]}...")
        print(f"{'='*70}")

        try:
            workflow_id = support_workflow.execute(workflow_input=ticket)
            workflow_ids.append(workflow_id)

            print(f"\n✅ Workflow started!")
            print(f"   Workflow ID: {workflow_id}")
            print(f"   View in UI: {config.host.replace('/api', '')}/execution/{workflow_id}")

        except Exception as e:
            print(f"\n❌ Error executing workflow: {e}")

    # Summary
    print(f"\n\n{'='*70}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*70}")
    print(f"Total tickets processed: {len(workflow_ids)}")
    print(f"\nWorkflow IDs:")
    for i, wf_id in enumerate(workflow_ids, 1):
        print(f"  {i}. {wf_id}")

    print(f"\n💡 To monitor workflows:")
    print(f"   - Visit the Orkes UI: {config.host.replace('/api', '')}")
    print(f"   - Navigate to 'Executions' to see live progress")
    print("\n✨ Done!")


if __name__ == "__main__":
    main()
