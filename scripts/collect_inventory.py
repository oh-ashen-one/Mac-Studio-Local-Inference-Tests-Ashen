#!/usr/bin/env python3
"""Read-only macOS inventory; emit only an explicit public-safe field allowlist."""
import argparse
import datetime
import json
import plistlib
import subprocess


def run(*args):
    return subprocess.check_output(args, timeout=90)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--machine-id', required=True,
                        help='Public alias, e.g. studio-old; do not use a hostname')
    args = parser.parse_args()
    data = json.loads(run('system_profiler', 'SPHardwareDataType',
                          'SPDisplaysDataType', '-json'))
    hw = data['SPHardwareDataType'][0]
    gpus = data.get('SPDisplaysDataType', [])
    # Never serialize the raw profiler objects: they contain serials and UUIDs.
    disks = []
    disk_list = plistlib.loads(run('diskutil', 'list', '-plist', 'internal', 'physical'))
    for disk in disk_list.get('AllDisksAndPartitions', []):
        identifier = disk.get('DeviceIdentifier')
        if identifier:
            info = plistlib.loads(run('diskutil', 'info', '-plist', identifier))
            disks.append({'capacity_bytes': info.get('TotalSize'),
                          'solid_state': info.get('SolidState'),
                          'bus_protocol': info.get('BusProtocol')})
    result = {
        'machine_id': args.machine_id,
        'status': 'directly_observed',
        'captured_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': 'Read-only local system_profiler, sysctl, sw_vers and diskutil',
        'model_name': hw.get('machine_name'),
        'model_identifier': hw.get('machine_model'),
        'chip': hw.get('chip_type'),
        'cpu_cores_description': hw.get('number_processors'),
        'memory_label': hw.get('physical_memory'),
        'memory_bytes': int(run('sysctl', '-n', 'hw.memsize').strip()),
        'gpus': [{'chip': g.get('sppci_model'),
                  'cores': g.get('sppci_cores'),
                  'metal_support': g.get('spdisplays_metal')}
                 for g in gpus],
        'os_version': run('sw_vers', '-productVersion').decode().strip(),
        'os_build': run('sw_vers', '-buildVersion').decode().strip(),
        'internal_physical_disks': disks,
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
