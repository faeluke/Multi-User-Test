class EfficiencyTestBench:
    """Coordinates physical test execution and understands lab topology"""

    def __init__(self, bench_config_path):
        self.config_path = bench_config_path
        self.vin_source = None
        self.vdrv_source = None
        self.vctrl_source = None
        self.daq = None
        self.vin_measure = None
        self.iin_measure = None
        self.vout_measure = None
        self.iout_measure = None
        self.vdrv_measure_source = None
        self.idrv_measure_source = None        
        self.vctrl_measure_source = None
        self.ictrl_measure_source = None
        

        #build the bench setup on startup
        self._build_bench()

    def _build_bench(self):
        """Parses configuration and relies on factory to plug in hardware."""
        
        print(f"\n--- Loading Bench Configuration: {self.config_path} ---")
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
            
        instruments = config["instruments"]
        
        # Dynamically build every single physical instrument mapped in your YAML
        self.vin_source = IntrumentFactory.create_instrument(
            module_name=instruments["vin_source"]["module_name"],
            class_name=instruments["vin_source"]["class_name"],
            connection=instruments["vin_source"]["connection"],
            safety_limits=instruments["vin_source"].get("safety_limits")
        )
        
        self.vdrv_source = IntrumentFactory.create_instrument(
            module_name=instruments["vdrv_source"]["module_name"],
            class_name=instruments["vdrv_source"]["class_name"],
            connection=instruments["vdrv_source"]["connection"],
            safety_limits=instruments["vdrv_source"].get("safety_limits")
        )
         
        self.vin_measure = IntrumentFactory.create_instrument(
            module_name=instruments["Meter1"]["module_name"],
            class_name=instruments["Meter1"]["device"],
            connection=instruments["Meter1"]["address"],
        )
        # insert if statement to use DAQ
        # insert code to allow different meters to be connected to be connected to different signals
        #       
        self.iin_measure = IntrumentFactory.create_instrument(
            module_name=instruments["Meter2"]["module_name"],
            class_name=instruments["Meter2"]["device"],
            connection=instruments["Meter2"]["address"],
        )
              
        self.vin_measure = IntrumentFactory.create_instrument(
            module_name=instruments["Meter3"]["module_name"],
            class_name=instruments["Meter3"]["device"],
            connection=instruments["Meter3"]["address"],
        )
              
        self.vin_measure = IntrumentFactory.create(
            module_name=instruments["Meter4"]["module_name"],
            class_name=instruments["Meter4"]["device"],
            connection=instruments["Meter4"]["address"],
        )
       
        self.e_load = IntrumentFactory.create(
            module_name=instruments["e_load"]["module_name"],
            class_name=instruments["e_load"]["class_name"],
            connection=instruments["e_load"]["connection"],
            safety_limits=instruments["vdrv_source"].get("safety_limits")
        )
        print("--- Bench Setup Initialization Complete ---\n")    

    def execute_efficiency_point(self, v_in, v_drv, i_out):
        """Sets hardware parameters, waits for settlement, and takes data."""
        self.vin_source.set_voltage(v_in)
        self.vdrv_source.set_voltage(v_drv)
        self.e_load.set_current(i_out)
        
        # Settle hardware transients before reading
        time.sleep(0.05) 
        
        measured_v_out = self.dmm.read_voltage()
        
        # Math: Simple simulated efficiency tracking
        power_in = v_in * i_out * 1.04 
        power_out = measured_v_out * i_out
        efficiency = (power_out / power_in) * 100 if power_in > 0 else 0
        
        return efficiency

@pytest.fixture(scope="session")
def bench():
    yaml_path = os.path.join(os.path.dirname(__file__), "bench_setup.yaml")
    test_bench = EfficiencyTestBench(yaml_path)
    
    yield test_bench
    
    print("\n[TEARDOWN] Disabling outputs and cleaning up physical connections.")
    test_bench.e_load.set_current(0)
    test_bench.vin_source.set_voltage(0)




class TestBench:

    # 



def bench_config():
    """Automatically finds and parses the local bench_config.yaml file."""
    config_filename = test_bench_config
    
    # Verify the file actually exists before trying to read it
    if not os.path.exists(config_filename):
        raise FileNotFoundError(
            f"Missing required configuration file: '{config_filename}' in the root directory. "
            f"Please create one based on your local bench hardware setup."
        )
        
    with open(config_filename, "r") as f:
        bench = yaml.safe_load(f)

    instruments =bench["Instruments"]

    module_name = insturments[]
