
import yaml

# Acquire static values once during initial test parsing
with open("config.yaml", "r") as f:
    _cfg = yaml.safe_load(f)["test_sweeps"]["efficiency_matrix"]
FIXED_AUX = _cfg["v_ctrl"]

def test_run_efficiency_sweep(bench, input_voltage, driver_voltage, output_current):
    """
    Purely declarative efficiency routine. Completely decoupled 
    from hardware changes or matrix modifications.
    """
    # 1. Drive target stimulus profile parameters
    bench.driver_source.set_voltage(driver_voltage)
    bench.input_source.set_voltage(input_voltage)
    bench.system_load.set_current(output_current)
    
    # 2. Grab unified readings tracking physical shunt math seamlessly
    metrics = bench.meters.read_power_data()

 
    # 3. Process Power Metrics
    power_in = metrics["vin"] * metrics["iin"]
    power_out = metrics["vout"] * metrics["iout"]
    
    assert power_in > 0, "Input power boundary error detected"
    efficiency = (power_out / power_in) * 100
    
    print(f"\n -> Calculated Efficiency for point: {efficiency:.2f}%")
    
    # 4. Standard Assert Boundary
    assert efficiency > 0.0  # Swap with your actual pass/fail threshold
