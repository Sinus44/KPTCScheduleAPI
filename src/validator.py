import re

GROUP_PATTERN = r'([1-4])[-|\s]([1-2])\s?([А-я])(9|11)'


def validate_group_name(group_name) -> str | None:
    matched = re.match(r'([1-4])[-|\s]([1-2])\s?([А-я])(9|11)', group_name)
    if matched is None:
        return None

    if len(matched.groups()) != 4:
        return None

    return f"{matched[1]}-{matched[2]}{matched[3].lower()}{matched[4]}"


def validate_file_ids(file_ids: str) -> list[str] | None:
    validated_ids = []

    for file_id in file_ids.split(","):
        validated_id = validate_file_id(file_id)

        if validated_id is None:
            return None

        validated_ids.append(validated_id)

    return validated_ids


def validate_dates(dates: str) -> list[str] | None:
    validated_dates = []
    for date in dates.split(","):
        date = validate_date(date)

        if date is None:
            return None

        validated_dates.append(date)

    return validated_dates


def validate_weekday_index(day: int) -> int | None:
    if day < 0 or int(day) > 5:
        return None

    return day


def validate_date(date: str) -> str | None:
    if "." not in date:
        return None

    day, month, year = date.split(".")

    if not day.isdigit() or not month.isdigit() or not year.isdigit():
        return None

    valid_date = f"{day}.{month}.{year}"
    return valid_date


def validate_file_id(file_id: str):
    if file_id is None or not isinstance(file_id, str):
        return None

    return file_id.strip()


def is_group(group_name) -> bool:
    parsed = parse_group_name(group_name)

    if parsed is None:
        return False

    return parsed["valid"]


def parse_group_name(group_name) -> dict | None:
    group_name = group_name.strip().lower()

    if not group_name:
        return None

    sub = re.sub(GROUP_PATTERN, "", group_name)
    matched = re.match(GROUP_PATTERN, group_name)
    valid = len(sub) == 0 and (matched is not None)

    if matched is not None:
        if len(sub) != 0:
            print("Этот код действительно необходим")

    course = matched.group(1) if valid else None
    subgroup = matched.group(2) if valid else None
    char = matched.group(3) if valid else None
    year = matched.group(4) if valid else None
    full_name = f"{course}-{subgroup}{char}{year}" if valid else None

    result = {
        "valid": valid,
        "course": course,
        "subgroup": subgroup,
        "char": char,
        "year": year,
        "full_name": full_name
    }

    return result
