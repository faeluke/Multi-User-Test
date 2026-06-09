import pytest
import yaml
from hardware_drivers import ShuntSetupTester, DirectSupplyTester

# Load global configuration
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

@pytest.fixture(scope="session")
def hardware():
    """Dynamically instantiates the driver based on the active setup."""
    setup_type = config.get("active_setup", "shunt")
    
    if setup_type == "shunt":
        tester = ShuntSetupTester()
    elif setup_type == "direct_supply":
        tester = DirectSupplyTester()
    else:
        raise ValueError(f"Unknown hardware setup configuration: {setup_type}")
        
    # Initialize global settings
    tester.configure_input_voltage(config["voltage_in"])
    yield tester
    
    # Teardown: Ensure everything turns off safely
    tester.set_load(0)