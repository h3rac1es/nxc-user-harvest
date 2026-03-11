#!/usr/bin/env python3
import re
import sys

SKIP_USERS = {'Guest', 'krbtgt'}

def parse_users(filename):
    users = []
    seen = set()

    with open(filename, 'r') as f:
        for line in f:
            username = None

            # Format 1: SidTypeUser format
            # e.g. 1000: RETRO2\admin (SidTypeUser)
            if 'SidTypeUser' in line:
                match = re.search(r'\d+: \S+\\(\S+) \(SidTypeUser\)', line)
                if match:
                    username = match.group(1)

            # Format 2: Password list format (with -Last PW Set- column)
            # e.g. SMB  10.x.x.x  445  BLN01  Julie.Martin  2024-08-17 ...
            elif re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}|<never>', line):
                # Skip header line
                if '-Username-' in line or '-Last PW Set-' in line:
                    continue
                # Extract username (5th field after splitting)
                parts = line.strip().split()
                if len(parts) >= 5:
                    username = parts[4]

            # Filter and collect
            if username:
                if (username not in SKIP_USERS and
                    not username.endswith('$') and
                    not username.startswith('-') and
                    username not in seen):
                    users.append(username)
                    seen.add(username)

    return users


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else 'output.txt'

    users = parse_users(filename)

    print('\n'.join(users))

    out_file = 'users.txt'
    with open(out_file, 'w') as f:
        f.write('\n'.join(users))

    print(f'\n[+] Found {len(users)} users -> saved to {out_file}')
