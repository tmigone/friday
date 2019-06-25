import requests, logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components.climate import (ClimateDevice, PLATFORM_SCHEMA)
from homeassistant.components.climate.const import (
    STATE_HEAT, STATE_COOL, STATE_IDLE,
    SUPPORT_TARGET_TEMPERATURE, SUPPORT_OPERATION_MODE, SUPPORT_FAN_MODE)

__version__ = '1.0.0'
_LOGGER = logging.getLogger(__name__) 
DOMAIN = 'myhabeetat'
DEPENDENCIES = []


BASE_URL = 'https://myhabeetat-api.now.sh/api'

# Config validation
CONF_EMAIL = 'email'
CONF_PASSWORD = 'password'
CONF_HOME_ID = 'home_id'
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_EMAIL): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Required(CONF_HOME_ID): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup MyHabeetat platform."""
    
    # Get configuration values
    email = config.get(CONF_EMAIL)
    password = config.get(CONF_PASSWORD)
    home_id = config.get(CONF_HOME_ID)

    # Get auth token
    r = requests.post(url = BASE_URL + '/login', data = { 'email': email, 'password': password })
    data = r.json()
    _LOGGER.debug(data)

    # Bail out if auth error
    if data['status'] != 'ok':
        _LOGGER.error(data['message'])
        return
    else:
        token = data['token']

    # Get devices
    r = requests.post(url = BASE_URL + '/devices', data = { 'token': token, 'home': home_id })
    data = r.json()
    _LOGGER.debug(data)

    # Add entities
    if data['status'] == 'ok':
        add_entities(BGHSmartControl(hass, device, token) for device in data['devices'])
    else:
        _LOGGER.error(data['message'])

class BGHSmartControl(ClimateDevice):
    def __init__(self, hass, device, token):
        """Initialize a BGHSmartControl device."""
        
        # Device info
        self._id = device['id']
        self._home = device['home']
        self._model = device['model']
        self._name = device['name']
        self._endpoint = device['endpoint']
        self._token = token

        # Operation variables
        self._target_temperature = 20
        self._current_temperature = 20
        self._current_operation = STATE_IDLE
        self._current_fan_mode = 'AUTO'

        # Configuration variables
        self._unit = hass.config.units.temperature_unit
        self._support_flags = (SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE | SUPPORT_FAN_MODE)
        self._operation_list = [ STATE_HEAT, STATE_COOL, STATE_IDLE ]
        self._fan_list = [ 'SLOW', 'MID', 'HIGH', 'AUTO' ]

    def update(self):
        """Fetch new state data for this climate device."""
        r = requests.post(url = BASE_URL + '/status', data = { 'token': self._token, 'home': self._home, 'device': self._id })
        data = r.json()
        _LOGGER.debug(data)

        # Update operation variables
        if data['status'] == 'ok':
            self._target_temperature = data['devices']['targetTemperature']
            self._current_temperature = data['devices']['temperature']
            self._current_operation = self.mode_convert_to_ha(data['devices']['mode'])
            self._current_fan_mode = data['devices']['fanMode']
        else:
            _LOGGER.error(data['message'])

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        r = requests.post(url = BASE_URL + '/set', data = {
            'token': self._token,
            'model': self._model,
            'endpoint': self._endpoint,
            'mode': self.mode_convert_to_mh(operation_mode)
        })
        data = r.json()
        _LOGGER.debug(data)

        # Update current operation mode
        if data['devices']:
            self._current_operation = operation_mode
        else:
            _LOGGER.error('Could not set operation_mode')
    
    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        r = requests.post(url = BASE_URL + '/set', data = {
            'token': self._token,
            'model': self._model,
            'endpoint': self._endpoint,
            'fanMode': fan_mode
        })
        data = r.json()
        _LOGGER.debug(data)

        # Update current fan mode
        if data['devices']:
            self._current_fan_mode = fan_mode
        else:
            _LOGGER.error('Could not set fan_mode')

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        temperature = kwargs.get('temperature')
        r = requests.post(url = BASE_URL + '/set', data = {
            'token': self._token,
            'model': self._model,
            'endpoint': self._endpoint,
            'targetTemperature': temperature
        })
        data = r.json()
        _LOGGER.debug(data)

        # Update current operation mode
        if data['devices']:
            self._current_temperature = temperature
        else:
            _LOGGER.error('Could not set temperature')

    @staticmethod
    def mode_convert_to_mh(operation):
        operations = {
            STATE_HEAT: 'HEAT',
            STATE_COOL: 'COOL',
            STATE_IDLE: 'OFF'
        }
        return operations.get(operation, 'OFF')

    @staticmethod
    def mode_convert_to_ha(mode):
        states = {
            'HEAT': STATE_HEAT,
            'COOL': STATE_COOL,
            'OFF': STATE_IDLE
        }
        return states.get(mode, STATE_IDLE)        

    @property
    def name(self):
        """Name of the device."""
        return self._name
    
    @property
    def current_temperature(self):
        """Return the sensor temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature
    
    @property
    def operation_list(self):
        """List of available operation modes."""
        return self._operation_list

    @property
    def current_operation(self):
        """Return the current operation mode."""
        return self._current_operation

    @property
    def fan_list(self):
        """List of available fan modes."""
        return self._fan_list

    @property
    def current_fan_mode(self):
        """Return the current fan mode."""
        return self._current_fan_mode

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def should_poll(self):
        """Polling is required."""
        return True

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._support_flags           