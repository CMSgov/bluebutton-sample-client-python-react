from typing import Dict
from ..configs.config import ConfigType


# based upon the environment variable for ENV set
# we can determine what the settings should be 
def get_config_settings(env) -> Dict :
    config_type = 'local'
    if (env in ('sandbox','development')):
        config_type = 'sandbox'
    elif (env == 'production'):
        config_type = 'production'

    return ConfigType.get(config_type)
