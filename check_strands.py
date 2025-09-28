#!/usr/bin/env python3
"""
Check available Strands imports
"""

try:
    import strands
    print("✅ strands imported successfully")
    print(f"Strands version: {getattr(strands, '__version__', 'unknown')}")
    print(f"Available attributes: {dir(strands)}")
except ImportError as e:
    print(f"❌ Failed to import strands: {e}")

try:
    from strands import Agent
    print("✅ Agent imported successfully")
except ImportError as e:
    print(f"❌ Failed to import Agent: {e}")

try:
    from strands.providers import BedrockProvider
    print("✅ BedrockProvider imported from strands.providers")
except ImportError as e:
    print(f"❌ Failed to import BedrockProvider from strands.providers: {e}")

try:
    from strands.core.providers import BedrockProvider
    print("✅ BedrockProvider imported from strands.core.providers")
except ImportError as e:
    print(f"❌ Failed to import BedrockProvider from strands.core.providers: {e}")

# Try to find the correct import path
try:
    import strands.core
    print(f"strands.core attributes: {dir(strands.core)}")
except ImportError as e:
    print(f"❌ Failed to import strands.core: {e}")

# Check for other possible locations
import pkgutil
print("\nAvailable strands submodules:")
for importer, modname, ispkg in pkgutil.iter_modules(strands.__path__, strands.__name__ + "."):
    print(f"  {modname}")
