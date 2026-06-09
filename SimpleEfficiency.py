@pytest.mark.parametrize("load_current", config["load_currents"])
def test_power_supply_efficiency(hardware, load_current):
    # Apply identical parameter step to whatever hardware is plugged in
    hardware.set_load(load_current)
    
    # Extract data maps uniformly
    metrics = hardware.measure_metrics()
    
    p_in = metrics["v_in"] * metrics["i_in"]
    p_out = metrics["v_out"] * metrics["i_out"]
    efficiency = (p_out / p_in) * 100
    
    assert efficiency >= config["min_efficiency_percent"], \
        f"Failed on {config['active_setup']} setup at {load_current}A!"