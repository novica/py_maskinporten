# smoke_test.py

try:
    from pymaskinporten import main

    assert main() == "Hello from pymaskinporten!"
    print("Smoke test passed: App imported successfully!")
except ImportError as e:
    print(f"Smoke test failed: {e}")
    exit(1)
