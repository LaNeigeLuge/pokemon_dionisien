#!/usr/bin/env python3
"""
Map Analyzer Tool
Analyzes TMX map files and suggests collision boxes and door locations
"""

import pygame
import pytmx
import sys
import os

# Initialize pygame for pytmx
pygame.init()
pygame.display.set_mode((1, 1))  # Minimal display for loading

def analyze_map(tmx_path):
    """Analyze a TMX map and suggest collisions and doors"""
    try:
        tmx_data = pytmx.load_pygame(tmx_path)
    except Exception as e:
        print(f"Error loading map: {e}")
        return

    print(f"\n{'='*60}")
    print(f"Map Analysis: {os.path.basename(tmx_path)}")
    print(f"{'='*60}")
    print(f"Map Size: {tmx_data.width}x{tmx_data.height} tiles ({tmx_data.width*16}x{tmx_data.height*16} pixels)")
    print(f"Tile Size: {tmx_data.tilewidth}x{tmx_data.tileheight}")

    # List all layers
    print(f"\n📋 Layers ({len(tmx_data.layers)}):")
    for layer in tmx_data.layers:
        layer_type = type(layer).__name__
        print(f"  - {layer.name} ({layer_type})")

    # Analyze existing objects
    objects_list = list(tmx_data.objects)
    print(f"\n🔍 Existing Objects ({len(objects_list)}):")

    collisions = []
    switches = []
    spawns = []
    other_objects = []

    for obj in objects_list:
        if obj.name == "collision":
            collisions.append(obj)
        elif obj.name and obj.name.startswith("switch"):
            switches.append(obj)
        elif obj.name and obj.name.startswith("spawn"):
            spawns.append(obj)
        else:
            other_objects.append(obj)

    print(f"\n  Collisions: {len(collisions)}")
    if len(collisions) > 0 and len(collisions) <= 10:
        for col in collisions[:10]:
            print(f"    - ({int(col.x)}, {int(col.y)}) size: {int(col.width)}x{int(col.height)}")

    print(f"\n  🚪 Doors/Switches: {len(switches)}")
    for switch in switches:
        parts = switch.name.split()
        target_map = parts[1] if len(parts) > 1 else "?"
        port = parts[2] if len(parts) > 2 else "?"
        print(f"    - {switch.name}")
        print(f"      Position: ({int(switch.x)}, {int(switch.y)}) size: {int(switch.width)}x{int(switch.height)}")
        print(f"      → Goes to: {target_map}.tmx (port {port})")

    print(f"\n  📍 Spawn Points: {len(spawns)}")
    for spawn in spawns:
        parts = spawn.name.split()
        source_map = parts[1] if len(parts) > 1 else "?"
        port = parts[2] if len(parts) > 2 else "?"
        print(f"    - {spawn.name}")
        print(f"      Position: ({int(spawn.x)}, {int(spawn.y)})")
        print(f"      ← From: {source_map}.tmx (port {port})")

    if other_objects:
        print(f"\n  Other Objects: {len(other_objects)}")
        for obj in other_objects[:5]:
            print(f"    - {obj.name if obj.name else 'unnamed'} at ({int(obj.x)}, {int(obj.y)})")

    # Check for door/spawn consistency
    print(f"\n{'='*60}")
    print("🔗 Door-Spawn Link Verification:")
    print(f"{'='*60}")

    for switch in switches:
        parts = switch.name.split()
        if len(parts) >= 3:
            target_map = parts[1]
            port = parts[2]

            # Check if target map exists
            map_dir = os.path.dirname(tmx_path)
            target_path = os.path.join(map_dir, f"{target_map}.tmx")

            if os.path.exists(target_path):
                print(f"\n✓ Door: {switch.name}")
                print(f"  Target map exists: {target_map}.tmx")

                # Load target map and check for spawn
                try:
                    target_tmx = pytmx.load_pygame(target_path)
                    current_map_name = os.path.basename(tmx_path).replace('.tmx', '')
                    expected_spawn = f"spawn {current_map_name} {port}"

                    spawn_found = False
                    for obj in target_tmx.objects:
                        if obj.name == expected_spawn:
                            spawn_found = True
                            print(f"  ✓ Spawn point found: {expected_spawn} at ({int(obj.x)}, {int(obj.y)})")
                            break

                    if not spawn_found:
                        print(f"  ⚠️  WARNING: Spawn point missing in {target_map}.tmx!")
                        print(f"     Expected: '{expected_spawn}'")
                except Exception as e:
                    print(f"  ⚠️  Could not verify spawn: {e}")
            else:
                print(f"\n✗ Door: {switch.name}")
                print(f"  ⚠️  ERROR: Target map not found: {target_path}")

    print(f"\n{'='*60}")
    print("✅ Analysis Complete")
    print(f"{'='*60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python map_analyzer.py <map.tmx>")
        print("   or: python map_analyzer.py all")
        sys.exit(1)

    if sys.argv[1] == "all":
        # Analyze all maps in the map directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        map_dir = os.path.join(script_dir, "..", "pokemondionisien", "assets", "map")

        if not os.path.exists(map_dir):
            print(f"Map directory not found: {map_dir}")
            sys.exit(1)

        tmx_files = [f for f in os.listdir(map_dir) if f.endswith('.tmx')]
        tmx_files.sort()

        print(f"Found {len(tmx_files)} map files")

        for tmx_file in tmx_files:
            analyze_map(os.path.join(map_dir, tmx_file))
    else:
        tmx_path = sys.argv[1]
        if not os.path.exists(tmx_path):
            print(f"File not found: {tmx_path}")
            sys.exit(1)

        analyze_map(tmx_path)


if __name__ == "__main__":
    main()
