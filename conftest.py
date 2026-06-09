python import pytest
import yaml

# 1. Load test parameters from configuration
with open("Test.yaml", "r") as f:
    config = yaml.safe_load(f)

# Mock instrument class representing your PyVISA hardware control
class PowerSupplyTester:
    def set_input_voltage(self, voltage): pass
    def set_load_current(self, current): pass
    def measure_input_power(self): return 12.0 * 1.1 # Dummy P_in
    def measure_output_power(self, target_current): return 12.0 * target_current # Dummy P_out

# 2. Setup hardware fixture (runs once per test session)
@pytest.fixture(scope="session")
def hardware():
    tester = PowerSupplyTester()
    # Initialize instruments (e.g., rm.open_resource() via PyVISA)
    tester.set_input_voltage(config["voltage_in"])
    yield tester
    # Teardown: Turn off outputs safely when done
    tester.set_load_current(0)

# 3. Parametrization expands this into 5 distinct test runs
@pytest.mark.parametrize("load_current", config["load_currents"])
def test_power_supply_efficiency(hardware, load_current):
    # Apply load parameter
    hardware.set_load_current(load_current)
    
    # Read instrument data
    p_in = hardware.measure_input_power()
    p_out = hardware.measure_output_power(load_current)
    
    # Calculate efficiency
    efficiency = (p_out / p_in) * 100
    
    # Assert result against limits
    assert efficiency >= config["min_efficiency_percent"], \
        f"Failed at {load_current}A: Efficiency was {efficiency:.2f}%"