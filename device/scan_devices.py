"""
Simple Bluetooth device scanner to find Omi glasses
"""
import asyncio
from bleak import BleakScanner


async def scan_devices():
    """Scan for nearby Bluetooth devices"""
    print("🔍 Scanning for Bluetooth devices...")
    print("(This will take 5 seconds)\n")

    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("❌ No Bluetooth devices found!")
        print("\nTroubleshooting:")
        print("1. Make sure your Omi glasses are powered on")
        print("2. Make sure Bluetooth is enabled on your Mac")
        print("3. Try resetting your glasses")
        return

    print(f"✅ Found {len(devices)} device(s):\n")

    for i, device in enumerate(devices, 1):
        print(f"{i}. {device.name or 'Unknown'}")
        print(f"   MAC: {device.address}")
        print(f"   RSSI: {device.rssi} dBm")

        # Check if this is the Omi device
        if device.address == "9FFBF14A-4510-DFCE-A684-AB3362EE6B6A":
            print("   ⭐ THIS IS YOUR OMI DEVICE!")

        print()


if __name__ == "__main__":
    asyncio.run(scan_devices())
