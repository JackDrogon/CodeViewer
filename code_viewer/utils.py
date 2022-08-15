# coding: utf-8


def remove_anon(name: str) -> str:
    # if scope split by ::, any one contains str startwiths "__anon", remove it
    # like leveldb::__anon2cdfda410111::PosixEnv => leveldb::PosixEnv
    for field in name.split("::"):
        if field.startswith("__anon"):
            name = name.replace(f"{field}::", "")
    return name
