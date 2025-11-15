"""
Test script to verify Dadd-E setup
Run: uv run python test_setup.py
"""
import sys


def test_imports():
    """Test that all major dependencies can be imported"""
    print("🧪 Testing imports...")

    tests = [
        ("FastAPI", "from fastapi import FastAPI"),
        ("Uvicorn", "import uvicorn"),
        ("OpenAI", "from openai import AsyncOpenAI"),
        ("Deepgram", "from deepgram import Deepgram"),
        ("Composio", "from composio_openai import ComposioToolSet"),
        ("Supabase", "from supabase import create_client"),
        ("Redis", "import redis"),
        ("Omi SDK", "from omi import OmiOpusDecoder"),
        ("App Services", "from app.services.voice import VoiceService"),
        ("App Services", "from app.services.vision import VisionService"),
        ("App Services", "from app.services.integrations import IntegrationService"),
        ("App Services", "from app.services.database import DatabaseService"),
        ("FastAPI App", "from app.main import app"),
    ]

    passed = 0
    failed = 0

    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    return passed, failed


def test_env_file():
    """Check if .env file exists"""
    print("\n🔧 Checking environment...")

    import os
    from pathlib import Path

    env_file = Path(".env")
    if env_file.exists():
        print("  ✅ .env file exists")

        # Check for required keys
        with open(env_file) as f:
            content = f.read()

        required_keys = [
            "OPENAI_API_KEY",
            "DEEPGRAM_API_KEY",
            "COMPOSIO_API_KEY",
            "SUPABASE_URL",
            "SUPABASE_KEY",
        ]

        for key in required_keys:
            if key in content and "your_" not in content.split(key)[1].split("\n")[0]:
                print(f"  ✅ {key} is set")
            else:
                print(f"  ⚠️  {key} needs to be configured")
    else:
        print("  ⚠️  .env file not found - copy from .env.example")


def test_opus_library():
    """Test if Opus library is available"""
    print("\n🎧 Checking Opus library...")

    try:
        from opuslib import Decoder

        print("  ✅ Opus library is available")
    except Exception as e:
        print(f"  ❌ Opus library issue: {e}")
        print("  💡 Run: brew install opus")
        print("  💡 Or: conda install -c conda-forge opus libopus")


def main():
    print("🚀 Dadd-E Setup Test\n")
    print("=" * 50)

    # Test imports
    passed, failed = test_imports()

    # Test environment
    test_env_file()

    # Test Opus
    test_opus_library()

    # Summary
    print("\n" + "=" * 50)
    print(f"\n📊 Summary: {passed} passed, {failed} failed")

    if failed == 0:
        print("\n✅ All tests passed! Ready to run Dadd-E")
        print("\n🚀 Next steps:")
        print("  1. Configure your .env file with API keys")
        print("  2. Run: uv run main.py")
        print("  3. Visit: http://localhost:8000/docs")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
