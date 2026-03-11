# nxc-user-harvest

A simple but effective Python script to extract domain usernames from **NetExec (nxc) / CrackMapExec (cme)** SMB enumeration output.

Supports both output formats produced by nxc automatically — no flags needed.

---

## Features

- ✅ Supports **RID brute** output (`--rid-brute`)
- ✅ Supports **user enumeration** output (`--users`)
- ✅ Works with **mixed files** (both formats in one file)
- ✅ Skips system accounts (`Guest`, `krbtgt`)
- ✅ Skips machine accounts (ending with `$`)
- ✅ Deduplicates entries automatically
- ✅ Saves clean list to `users.txt`

---

## Supported Input Formats

**Format 1 — RID Brute** (`nxc smb <target> ... --rid-brute`)
```
SMB  10.10.10.10  445  DC01  1105: DOMAIN\Julie.Martin (SidTypeUser)
SMB  10.10.10.10  445  DC01  1106: DOMAIN\Clare.Smith (SidTypeUser)
```

**Format 2 — User Enumeration** (`nxc smb <target> ... --users`)
```
SMB  10.10.10.10  445  DC01  Administrator  2024-08-17 11:21:50  0  Built-in account...
SMB  10.10.10.10  445  DC01  Julie.Martin   2024-08-17 11:35:40  0
```

---

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/nxc-user-harvest
cd nxc-user-harvest
```

No dependencies — standard library only.

---

## Usage

**Step 1 — Save nxc output to a file:**
```bash
# RID brute
nxc smb <target> -u <user> -p <pass> --rid-brute | tee rid_output.txt

# User enumeration
nxc smb <target> -u <user> -p <pass> --users | tee users_output.txt
```

**Step 2 — Parse it:**
```bash
python3 parse_users.py rid_output.txt
python3 parse_users.py users_output.txt
```

**Output:**
```
Administrator
admin
Julie.Martin
Clare.Smith
Laura.Davies
...

[+] Found 24 users -> saved to users.txt
```

The clean username list is saved to `users.txt` in the current directory, ready to use with tools like `kerbrute`, `nxc`, `hydra`, etc.

---

## Example Workflow

```bash
# 1. Enumerate users
nxc smb 10.10.10.10 -u ldapreader -p 'Password123' --users | tee out.txt

# 2. Parse
python3 parse_users.py out.txt

# 3. Use with kerbrute
kerbrute userenum users.txt -d domain.local --dc 10.10.10.10

# 4. Password spray
nxc smb 10.10.10.10 -u users.txt -p 'Password123' --continue-on-success
```

---

## Customization

To skip additional accounts, edit the `SKIP_USERS` set at the top of the script:

```python
SKIP_USERS = {'Guest', 'krbtgt', 'inventory', 'ldapreader'}
```

---

## Contributing

Pull requests are welcome. If nxc changes its output format in a future version, feel free to open an issue.

---

## License

MIT
