
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
    with open(test_bench_config, "r") as f:
        setup_data = yaml.safe_load(f)
        
    inst_configs = setup_data["Instruments"]
    setup_configs = setup_data["measurement_setup"]
    strategy = setup_data["measurement_strategy"]
    
    # Construct base stimulus instruments
    live_input_src = IntrumentFactory.create_instrument(inst_configs["Main_Source"])
    live_driver_src = IntrumentFactory.create_instrument(inst_configs["Aux_Source"])
    live_load = IntrumentFactory.create_instrument(inst_configs["Load"])
    #live_ctrl_src = IntrumentFactory.create_instrument(inst_configs["Aux_Source"])
    live_ctrl_src=live_driver_src
    
    # Symmetrically construct chosen engine tracking shunts
    measurement_engine = IntrumentFactory.build_measurement_engine(strategy=strategy, inst_configs=inst_configs, setup_configs=setup_configs)
    
    active_bench = InstrumentBench(
        input_source=live_input_src,
        driver_source=live_driver_src,
        system_load=live_load,
        aux_source = live_ctrl_src,
        measurement_system=measurement_engine
        
    )

    #Turn it all On
    live_input_src.set_voltage_and_current(48,5)
    
    live_ctrl_src.set_voltage1(3.3,1)
    live_driver_src.set_voltage2(12,1)
    live_ctrl_src.enable_output()


    live_load.Set_Static_Current_L1(0.1)
    live_load.Set_Channel_Active('ON')
    live_load.Set_Load_Active()
    
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
            sweep["v_in"],
            sweep["v_drv"],
            sweep["i_out"]
        ))
        
        ids = [f"Vin={v_in}V,Vdrv={v_dr}V,Iout={i_out}A" for v_in, v_dr, i_out in combinations]
        metafunc.parametrize("input_voltage, driver_voltage, output_current", combinations, ids=ids)




 