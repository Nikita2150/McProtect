<div align="center">

[![Hackathon](https://img.shields.io/badge/hackathon-name-orange.svg)](https://tel-aviv.aitinkerers.org/p/ai-tinkerers-tel-aviv-the-big-mcp-hackathon)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

</div>

---

## 🏁 Getting Started <a name = "getting_started"></a>

### Prerequisites

- Python 3.11+
- pip

### Installing

1. Clone repository:

```
git clone https://github.com/Nikita2150/McProtect.git
cd McProtect
```

2. Create and fill `.env` file inside the `mcp_client` directory, as follows:

```
AZURE_OPENAI_ENDPOINT=ENTER_ENDPOINT
AZURE_OPENAI_API_KEY=ENTER_API_KEY
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME=ENTER_DEPLOYMENT_NAME
AZURE_OPENAI_API_VERSION=ENTER_OPENAI_API_VERSION
```

3. To setup client/servers:

```
cd ENTER_DIR_NAME_HERE
python -m venv venv              # create a virtual environment
venv\Scripts\activate            # activate virtual environment
pip install -r requirements.txt  # install all pip requirements
```

replace the ENTER_DIR_NAME_HERE with the relevant directory name (`mcp_client`, `weather_server` or `verify_server`)

## 🎈 Usage <a name="usage"></a>

To use the system, you have to run your wanted servers (using their virtual environments),

```
python weather.py
python verify.py
```

and then run the client,

```
python mcp_client.py
```
