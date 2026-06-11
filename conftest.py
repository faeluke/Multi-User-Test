import os
import pytest
import yaml
import pyvisa
from drivers.chroma import ChromaPSU
from drivers.hp import HPPSU

@pytest.fixture(scope="session")
def bench_config():
    """Automatically finds and parses the local bench_config.yaml file."""
    config_filename = "bench_config.yaml"
    
    # Verify the file actually exists before trying to read it
    if not os.path.exists(config_filename):
        raise FileNotFoundError(
            f"Missing required configuration file: '{config_filename}' in the root directory. "
            f"Please create one based on your local bench hardware setup."
        )
        
    with open(config_filename, "r") as f:
        return yaml.safe_load(f)

@pytest.fixture(scope="session")
def psu(bench_config):
    """Dynamically initializes the PSU based on the local YAML file layout."""
    psu_config = bench_config["instruments"]["power_supply"]
    brand = psu_config["brand"].lower()
    address = psu_config["address"]
    
    # Connect to the VISA subsystem
    rm = pyvisa.ResourceManager()
    resource = rm.open_resource(address)
    
    # Factory selection based on file contents
    if brand == "chroma":
        driver = ChromaPSU(resource, psu_config)
    elif brand == "hp":
        driver = HPPSU(resource, psu_config)
    else:
        resource.close()
        raise ValueError(f"Unsupported PSU brand found in your local YAML: {brand}")
        
    yield driver
    
    # Tear down hardware connection safely when testing concludes
    try:
        driver.enable_output(False)
    finally:
        resource.close()