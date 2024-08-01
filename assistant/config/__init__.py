import os
import yaml

user_profile_path = os.path.expanduser('~')

class Config:
    def __init__(self, config_path=f'{user_profile_path}/.assistant/config.yaml'):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        self._replace_env_vars(self.config)

    def _replace_env_vars(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                self._replace_env_vars(value)
            elif isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                config[key] = os.getenv(env_var, '')

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            value = value.get(k, default)
            if value is None:
                return default
        return value

    def set_env_if_not_exists(self, env_var, value):
        if not os.getenv(env_var):
            os.environ[env_var] = value

# Load the configuration
config = Config()

# Set the environment variables only if they are not already set
config.set_env_if_not_exists('OPENAI_API_KEY', config.get('openai.api_key'))
config.set_env_if_not_exists('INSTAGRAM_ACCESS_TOKEN', config.get('instagram.access_token'))
config.set_env_if_not_exists('CLIENT_ID', config.get('reddit.id'))
config.set_env_if_not_exists('CLIENT_SECRET', config.get('reddit.secret'))
config.set_env_if_not_exists('USER_AGENT', config.get('reddit.user_agent'))
config.set_env_if_not_exists('ALPHAVANTAGE_KEY', config.get('alphavantage.key'))
config.set_env_if_not_exists('GPT_DIRECTIONS', config.get('gpt_directions'))
