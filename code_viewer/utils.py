# coding: utf-8

from dataclasses import fields


def remove_anon(name: str) -> str:
    # if scope split by ::, any one contains str startwiths "__anon", remove it
    # like leveldb::__anon2cdfda410111::PosixEnv => leveldb::PosixEnv
    for index, field in enumerate(name.split('::')):
        if not field.startswith("__anon"):
            continue

        if index == 0:
            name = name.replace(field, "")
        else:
            name = name.replace(f"::{field}", "")
    return name
