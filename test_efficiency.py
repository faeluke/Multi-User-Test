
import yaml
import time

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
    bench.driver_source.set_voltage2(driver_voltage,1)
    bench.input_source.set_voltage_and_current(input_voltage,output_current *5)
    bench.system_load.Set_Static_Current_L1(output_current)
    time.sleep(10)

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
