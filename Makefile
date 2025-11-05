.PHONY: help setup install run run-notebook convert clean

help:
	@echo "Multi-Agent Workflow - Available Commands"
	@echo "=========================================="
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Create conda environment and install dependencies"
	@echo "  make install        - Install dependencies only (assumes env exists)"
	@echo ""
	@echo "Running:"
	@echo "  make run            - Run workflow from Python script (CLI)"
	@echo "  make run-notebook   - Execute notebook from terminal"
	@echo "  make convert        - Convert notebook to Python script"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove generated files"
	@echo ""

setup:
	@echo "Creating conda environment..."
	conda create -n orkes-multiagent python=3.11 -y
	@echo "Installing dependencies..."
	conda run -n orkes-multiagent pip install conductor-python openai requests python-dotenv ipykernel jupyter nbconvert
	@echo "Registering Jupyter kernel..."
	conda run -n orkes-multiagent python -m ipykernel install --user --name=orkes-multiagent --display-name="Python (orkes-multiagent)"
	@echo "✅ Setup complete! Don't forget to create your .env file:"
	@echo "   cp .env.example .env"
	@echo "   # Then edit .env with your credentials"

install:
	@echo "Installing dependencies..."
	conda run -n orkes-multiagent pip install conductor-python openai requests python-dotenv ipykernel jupyter nbconvert
	@echo "✅ Dependencies installed"

run:
	@echo "Running workflow from Python script..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found"; \
		echo "   cp .env.example .env"; \
		echo "   # Then edit .env with your credentials"; \
		exit 1; \
	fi
	conda run -n orkes-multiagent python run_workflow.py

run-notebook:
	@echo "Executing notebook from terminal..."
	@if [ ! -f .env ]; then \
		echo "❌ Error: .env file not found"; \
		echo "   cp .env.example .env"; \
		echo "   # Then edit .env with your credentials"; \
		exit 1; \
	fi
	conda run -n orkes-multiagent jupyter nbconvert --to notebook --execute --inplace technical-implementation.ipynb
	@echo "✅ Notebook executed. Check technical-implementation.ipynb for results"

convert:
	@echo "Converting notebook to Python script..."
	conda run -n orkes-multiagent jupyter nbconvert --to python technical-implementation.ipynb
	@echo "✅ Created technical-implementation.py"

clean:
	@echo "Cleaning generated files..."
	rm -f technical-implementation.py
	rm -rf __pycache__
	rm -rf .ipynb_checkpoints
	@echo "✅ Cleaned"
