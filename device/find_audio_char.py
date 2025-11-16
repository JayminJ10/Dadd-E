"""
Find the correct audio characteristic with notify capability
"""
import asyncio
from bleak import BleakClient

DEVICE_MAC = "9FFBF14A-4510-DFCE-A684-AB3362EE6B6A"


async def find_audio_characteristic():
    """Find characteristics that support notifications"""
    print(f"🔍 Scanning {DEVICE_MAC} for audio characteristics...\n")

    async with BleakClient(DEVICE_MAC) as client:
        print("✅ Connected!\n")

        notify_chars = []

        for service in client.services:
            print(f"📦 Service: {service.uuid}")
            print(f"   Description: {service.description}")

            for char in service.characteristics:
                properties = ", ".join(char.properties)
                print(f"\n   📌 Characteristic: {char.uuid}")
                print(f"      Handle: {char.handle}")
                print(f"      Properties: {properties}")

                # Check if it supports notify
                if "notify" in char.properties:
                    notify_chars.append(char)
                    print(f"      ⭐ CAN NOTIFY - Possible audio stream!")

                    # Try to read descriptor to get more info
                    for descriptor in char.descriptors:
                        print(f"         Descriptor: {descriptor.uuid}")

            print()

        print("\n" + "="*60)
        print("🎯 CHARACTERISTICS WITH NOTIFY CAPABILITY:")
        print("="*60)

        if notify_chars:
            for i, char in enumerate(notify_chars, 1):
                print(f"\n{i}. UUID: {char.uuid}")
                print(f"   Handle: {char.handle}")
                print(f"   Properties: {', '.join(char.properties)}")
                print(f"   Service: {char.service_uuid}")
        else:
            print("❌ No characteristics with notify capability found!")

        print("\n" + "="*60)
        print("💡 RECOMMENDATION:")
        print("="*60)

        # Look for custom Omi characteristics (19b10xxx pattern)
        omi_chars = [c for c in notify_chars if c.uuid.startswith("19b10")]
        if omi_chars:
            print(f"\n✅ Found {len(omi_chars)} Omi custom characteristic(s):")
            for char in omi_chars:
                print(f"   • {char.uuid}")
            print(f"\nTry using: {omi_chars[0].uuid}")
        else:
            print("\n⚠️  No Omi custom characteristics found with notify.")
            if notify_chars:
                print(f"Try the first notify characteristic: {notify_chars[0].uuid}")


if __name__ == "__main__":
    asyncio.run(find_audio_characteristic())
