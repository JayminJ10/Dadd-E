"""
Comprehensive Omi Glass Characteristic Scanner
Connects to all characteristics and monitors data flow
"""
import asyncio
from bleak import BleakScanner, BleakClient

DEVICE_MAC = "9FFBF14A-4510-DFCE-A684-AB3362EE6B6A"

async def scan_device():
    print(f"🔍 Scanning {DEVICE_MAC}...")

    async with BleakClient(DEVICE_MAC) as client:
        print(f"✅ Connected to {DEVICE_MAC}\n")

        # Get all services
        for service in client.services:
            print(f"📦 Service: {service.uuid}")
            print(f"   Description: {service.description}")

            # Get all characteristics for this service
            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"\n   📍 Characteristic: {char.uuid}")
                print(f"      Properties: {props}")
                print(f"      Description: {char.description}")

                # Try to read if readable
                if "read" in char.properties:
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        print(f"      Value: {value[:50] if len(value) > 50 else value}")
                    except Exception as e:
                        print(f"      Read error: {e}")

                # Monitor notifications if available
                if "notify" in char.properties:
                    print(f"      ⚡ Can notify - this might be audio!")
                    print(f"      UUID: {char.uuid}")

            print()

if __name__ == "__main__":
    asyncio.run(scan_device())
