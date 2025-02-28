def load_config():
    """Load configuration settings from the config.json file."""
    import json
    import os

    config_path = os.path.join(os.path.dirname(__file__), '../../config/config.json')
    
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    
    return config

def get_api_key():
    """Get the API key from the loaded configuration."""
    config = load_config()
    return config.get('api_key')

def get_default_settings():
    """Get default settings from the configuration."""
    config = load_config()
    return config.get('default_settings', {})