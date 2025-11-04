# Multi-Agent Customer Support Triage System with Orkes Conductor

This repository contains the complete implementation of a multi-agent AI system built with Orkes Conductor for automated customer support ticket triage.

## Contents

- **blog-post.md**: A comprehensive blog post (1,290 words) explaining the architecture, implementation, and benefits of building multi-agent systems with Orkes Conductor
- **technical-implementation.ipynb**: A Jupyter notebook with step-by-step technical implementation, including:
  - Environment setup
  - Agent definitions (Classifier, Knowledge, Escalation)
  - Custom worker task implementation
  - Workflow composition
  - Testing and monitoring examples

## Architecture Overview

The system orchestrates three specialized AI agents:

1. **Classifier Agent**: Analyzes incoming tickets to determine category, sentiment, and urgency
2. **Knowledge Agent**: Searches internal documentation and suggests solutions with confidence scores
3. **Escalation Agent**: Routes tickets to human agents based on urgency and confidence levels

Additionally, a **custom worker task** handles notifications to Slack, email, and PagerDuty when tickets are escalated.

## Key Features

- Multi-agent coordination using Orkes Conductor
- LLM integration via GPT-4 for intelligent classification and knowledge search
- Custom worker implementation demonstrating polling mechanism
- Conditional workflow logic based on urgency and confidence
- Production-ready patterns for error handling and monitoring

## Getting Started

### Prerequisites

- Python 3.11+
- Orkes Conductor account (free at [orkes.io](https://orkes.io/))
- OpenAI API key

### Installation

```bash
# Clone this repository
git clone <repository-url>
cd orkes-multiagent-exercise

# Install dependencies
pip install conductor-python openai requests python-dotenv

# Set up environment variables
export ORKES_KEY_ID="your-key-id"
export ORKES_KEY_SECRET="your-key-secret"
export OPENAI_API_KEY="your-openai-key"
```

### Running the Notebook

1. Open `technical-implementation.ipynb` in Jupyter
2. Update the configuration in Step 2 with your credentials
3. Run cells sequentially to:
   - Define agents
   - Create the workflow
   - Register the worker
   - Test with sample tickets

## How It Works

### Workflow Flow

```
Ticket Received → Classifier Agent → Knowledge Agent → Escalation Evaluation
                                                              ↓
                                            High Confidence: Auto-Resolve
                                            Low Confidence: Notify Team (Worker Task)
```

### Worker Task Integration

The custom worker demonstrates:
- Polling Conductor for tasks every 0.5 seconds
- Executing custom business logic (notifications)
- Reporting results back to Conductor
- Integration with external services (Slack, email, etc.)

## Use Cases

This architecture can be adapted for various scenarios:
- Marketing campaign automation
- Financial report generation
- Incident response automation
- Data pipeline orchestration
- Any multi-step workflow requiring intelligent coordination

## Learning Resources

- [Orkes Conductor Documentation](https://docs.conductor-oss.org/)
- [Multi-Agent Systems Patterns](https://orkes.io/blog/)
- Blog post in this repo: `blog-post.md`

## License

MIT

## Author

Created as part of the Orkes Content Engineer Exercise
