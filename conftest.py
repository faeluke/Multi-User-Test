
import pytest
import yaml
from itertools import product
from BenchSetup import IntrumentFactory
from MeasurementOptions import InstrumentBench


test_bench_config ="LukeBench.yaml"
#setup the output XLS File


@pytest.fixture(scope="session")
def bench():
    """
    Builds the entire bench architecture up front and ensures a safe teardown.
    """
    with open("bench_setup.yaml", "r") as f:
        setup_data = yaml.safe_load(f)
        
    inst_configs = setup_data["Instruments"]
    setup_configs = setup_data["measurement_setup"]
    strategy = setup_data["measurement_strategy"]
    
    # Construct base stimulus instruments
    live_input_src = IntrumentFactory.create_instrument(inst_configs["Main_Source"])
    live_driver_src = IntrumentFactory.create_instrument(inst_configs["Aux_Source"])
    live_load = IntrumentFactory.create_instrument(inst_configs["Load"])
    live_ctrl_src = IntrumentFactory.create_instrument(inst_configs["Aux_Source"])

    
    # Symmetrically construct chosen engine tracking shunts
    measurement_engine = IntrumentFactory.build_measurement_engine(strategy=strategy, inst_configs=inst_configs, setup_configs=setup_configs)
    
    active_bench = InstrumentBench(
        input_source=live_input_src,
        driver_source=live_driver_src,
        system_load=live_load,
        aux_source = live_ctrl_src,
        measurement_system=measurement_engine
        
    )
    
    yield active_bench
    active_bench.emergency_shutdown()



# Pytest hook to dynamically generate parameters for tests

def pytest_generate_tests(metafunc):
    """Dynamic Cartesian matrix expansion routine parsed straight from config.yaml."""
    required_params = ["input_voltage", "driver_voltage", "output_current"]
    if all(param in metafunc.fixturenames for param in required_params):
        
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        sweep = config["test_sweeps"]["efficiency_matrix"]
        
        combinations = list(product(
            sweep["input_voltages"],
            sweep["driver_voltages"],
            sweep["output_currents"]
        ))
        
        ids = [f"Vin={v_in}V,Vdrv={v_dr}V,Iout={i_out}A" for v_in, v_dr, i_out in combinations]
        metafunc.parametrize("input_voltage, driver_voltage, output_current", combinations, ids=ids)




