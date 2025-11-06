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
- Conda or Miniconda (recommended) - [Installation Guide](https://docs.conda.io/en/latest/miniconda.html)
  - Alternative: Python venv can be used instead
- Jupyter Notebook or JupyterLab
- Orkes Conductor account (free at [orkes.io](https://orkes.io/))
- OpenAI API key (configured in Orkes UI)

### Installation

```bash
# Clone this repository
git clone https://github.com/nicklotz/orkes-multiagent-workflow.git
cd orkes-multiagent-workflow

# Create conda environment (recommended)
conda create -n orkes-multiagent python=3.11 -y
conda activate orkes-multiagent

# Install dependencies
pip install conductor-python openai requests python-dotenv ipykernel

# Register the environment as a Jupyter kernel
python -m ipykernel install --user --name=orkes-multiagent --display-name="Python (orkes-multiagent)"

# Set up environment variables
cp .env.example .env
# Edit .env and add your Orkes credentials
```

**Alternative: Without Conda**

If you prefer not to use conda:

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install conductor-python openai requests python-dotenv jupyter

# Set up environment variables
cp .env.example .env
```

### Configuration

#### 1. Orkes Credentials (Required)

Create a `.env` file based on `.env.example`:

```bash
ORKES_SERVER_URL=https://play.orkes.io/api
ORKES_KEY_ID=your_key_id_here
ORKES_KEY_SECRET=your_key_secret_here
```

Get your credentials from:
1. Sign up at [orkes.io](https://orkes.io/)
2. Navigate to **Settings → Access Keys**
3. Create a new access key and copy the Key ID and Secret

#### 2. OpenAI Configuration (Required)

The OpenAI API key is **not stored in code**. Instead, configure it in your Orkes account:

1. Log into https://play.orkes.io/ (or your Orkes instance)
2. Navigate to **Settings → Integrations** (or **AI/LLM Providers**)
3. Add OpenAI as a provider and give it a name (e.g., "openai" or "nl-openai")
4. Enter your OpenAI API key
5. **Important:** Enable at least one model (e.g., "gpt-4", "gpt-4o", or "gpt-3.5-turbo")

**Then update the code:**
- In both `run_workflow.py` and the notebook, update `llm_provider="openai"` to match your integration name
- For example, if you named it "nl-openai", change to `llm_provider="nl-openai"`

This keeps your API keys secure and centralized.

### Running the Notebook

1. Ensure your `.env` file is configured (see above)
2. Start Jupyter:
   ```bash
   jupyter notebook
   # or
   jupyter lab
   ```
3. Open `technical-implementation.ipynb`
4. **Select the kernel**:
   - In Jupyter Notebook: `Kernel` → `Change Kernel` → `Python (orkes-multiagent)`
   - In JupyterLab: Click kernel name in top-right → Select `Python (orkes-multiagent)`
   - In VS Code: Click kernel selector → Choose `Python (orkes-multiagent)`
5. Run cells sequentially starting from Step 0 to:
   - Set up the conda environment (if not already done)
   - Install dependencies
   - Define agents
   - Create the workflow
   - Register the worker
   - Test with sample tickets

## Running the Workflow

You have multiple options for running this workflow:

### Option 1: Command Line Script (Fastest)

Run the standalone Python script directly from your terminal:

```bash
# Activate environment
conda activate orkes-multiagent

# Run the workflow
python run_workflow.py
```

This runs all test tickets and displays results in your terminal.

### Option 2: Using Makefile Commands

If you have `make` installed:

```bash
# One-time setup
make setup

# Run the workflow
make run

# Or execute the notebook from terminal
make run-notebook
```

See `make help` for all available commands.

### Option 3: Execute Notebook from Terminal

You can run the Jupyter notebook without opening the UI:

```bash
conda activate orkes-multiagent

# Execute notebook in-place (updates the notebook with outputs)
jupyter nbconvert --to notebook --execute --inplace technical-implementation.ipynb

# Or execute and create a new output file
jupyter nbconvert --to notebook --execute technical-implementation.ipynb --output executed-notebook.ipynb
```

### Option 4: Convert Notebook to Python Script

```bash
# Convert notebook to .py file
jupyter nbconvert --to python technical-implementation.ipynb

# Run the generated script
python technical-implementation.py
```

### Option 5: Interactive Notebook (Traditional)

For interactive exploration, use Jupyter as described in the "Running the Notebook" section above.

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
