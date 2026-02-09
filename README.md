# GiveAGo

A Python-based agent project built using **Google ADK (Agent Development Kit)** with web interface support.

## Project Structure

```
my_agent/
  __init__.py
  agent.py
  tools.py
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd GiveAGo
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Project

Can be run with:
- `adk run my_agent` - Run the agent
- `adk run web --port 8000` - Run the web version (access at http://localhost:8000)

## Development

Make sure your virtual environment is activated before working:
```bash
source venv/bin/activate
```

To deactivate the environment:
```bash
deactivate
```
