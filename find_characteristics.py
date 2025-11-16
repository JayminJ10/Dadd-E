"""
Find all characteristics for Omi Glass device
Run: python find_characteristics.py
"""
import asyncio
from bleak import BleakClient, BleakScanner


async def find_device_characteristics():
    """Find and print all characteristics of the Omi Glass device"""

    device_mac = "9FFBF14A-4510-DFCE-A684-AB3362EE6B6A"

    print(f"🔍 Searching for device: {device_mac}")
    print("Make sure your Omi Glass is powered on and nearby!\n")

    # Scan for the device
    print("📡 Scanning for devices...")
    device = await BleakScanner.find_device_by_address(device_mac, timeout=10.0)

    if not device:
        print(f"❌ Could not find device {device_mac}")
        print("\nTry running: omi-scan")
        return

    print(f"✅ Found device: {device.name}")
    print(f"   Address: {device.address}\n")

    # Connect and get characteristics
    print("🔌 Connecting to device...")
    async with BleakClient(device) as client:
        print("✅ Connected!\n")

        print("📋 Device Services and Characteristics:\n")
        print("=" * 80)

        for service in client.services:
            print(f"\n🔷 Service: {service.uuid}")
            print(f"   Description: {service.description}")

            for char in service.characteristics:
                print(f"\n   📌 Characteristic: {char.uuid}")
                print(f"      Properties: {', '.join(char.properties)}")
                print(f"      Description: {char.description}")

                # Check if this might be the audio characteristic
                if "notify" in char.properties or "read" in char.properties:
                    print(f"      ⭐ CANDIDATE for audio streaming!")

        print("\n" + "=" * 80)
        print("\n💡 Look for characteristics with 'notify' or 'read' properties")
        print("   These are likely candidates for audio streaming.")
        print("\n📝 Update your .env file with:")
        print("   OMI_AUDIO_CHAR_UUID=<uuid-from-above>")


if __name__ == "__main__":
    asyncio.run(find_device_characteristics())
