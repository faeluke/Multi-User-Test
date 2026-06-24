
efficiency_tester/
│
├── config.yaml               # Defines the test point sweeps and metrics
├── bench_setup.yaml          # Defines physical instrument connections & strategy
├── conftest.py               # Houses Pytest setup, teardown, and dynamic test injection
├── test_efficiency.py        # Core declarative test script
│
└── instruments/
    ├── __init__.py
    ├── base.py               # Abstract base classes and interfaces
    ├── factory.py            # Dynamic hardware instantiator
    ├── manager.py            # Active test bench container object
    └── measurement.py        # Concrete DAQ and Quad-DMM shunt engines