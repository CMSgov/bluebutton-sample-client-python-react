from typing import Dict
from ..configs.config import ConfigType


    # based upon the environment variable for ENV set
    # we can determine what the settings should be 

def getConfigSettings(env) -> Dict :
    if (env == 'local'):
        configType = 'local'
    elif (env in ('sandbox','development')):
        configType = 'sandbox'
    elif (env == 'production'):
        configType = 'production'
    else:
        configType = 'local'

    configDict = ConfigType.get(configType)

    return configDict