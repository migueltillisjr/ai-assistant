# ai-assistant
ai-assistant


## High Level Requirements
- python3.11
- Add add your assistant config file to ~/.assistant/config.yaml
```yaml
openai:
  api_key: ${OPENAI_API_KEY}
instagram:
  access_token: ${INSTAGRAM_ACCESS_TOKEN}
reddit:
  id: ${CLIENT_ID}
  secret: ${CLIENT_SECRET}
  user_agent: ${USER_AGENT}
alphavantage:
  key: ${ALPHAVANTAGE_KEY}
gpt_directions: ${GPT_DIRECTIONS}
ui_auth: ${UI_AUTH}
fine_tuning: ${FINE_TUNING}
```

## Example Ui Authentication file
```yaml
credentials:
  usernames:
    your_username:
      email: your_email@example.com
      password: your_password_hash

cookie:
  name: your_cookie_name
  key: your_cookie_key
  expiry_days: 30

preauthorized:
  emails:
    - preauthorized_user1@example.com
    - preauthorized_user2@example.com
```


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
