# ai-assistant
ai-assistant


## High Level Requirements
- python3.11
- export OPENAI_API_KEY="YOUR OPEN AI API KEY"
- export INSTAGRAM_ACCESS_TOKEN="YOUR INSTAGRAM ACCESS TOKEN"
- export GPT_DIRECTIONS="Location of GPT directions on disk"
- pip3.11 install -r requirements.txt

## Run it at the Cli
```shell
# Assistant
python3.11 -m assistant

# UI
cd ui/
streamlit run __main__.py

# API
python3.11 -m api
```
