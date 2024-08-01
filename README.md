# ai-assistant
ai-assistant


## High Level Requirements
- python3.11
- export OPENAI_API_KEY="YOUR OPEN AI API KEY"
- export INSTAGRAM_ACCESS_TOKEN="YOUR INSTAGRAM ACCESS TOKEN"
- export GPT_DIRECTIONS="Location of GPT directions on disk" -> point to assistant/files/chatgpt.directions.txt
- pip3.11 install -r requirements.txt

## Run it at the Cli
```shell
# Assistant
python3.11 -m assistant
python3.11 -m assistant.integrations.reddit
python3.11 -m assistant.integrations.alpha_advantage

# UI, login info location -> ui/.streamlit/secrets.toml
cd assistant/ui/
streamlit run __main__.py

# API
python3.11 -m api
```
