def time_string_to_mins(string):
    split1 = string.split(" ")
    split2 = split1[0].split(":")

    am_or_pm = split1[1]

    hours = (int(split2[0]))
    if hours == 12:
        hours = 0
    else:
        hours *= 60
    mins = int(split2[1])
    if am_or_pm == "PM":
        hours += 12 * 60

    total_mins = hours + mins
    return total_mins


def mins_to_time_string(time):
    mins = int(time % 60)
    hours = int((time - mins) / 60)
    am_or_pm = "AM"
    if hours == 0:
        hours = 12
    elif hours > 12:
        am_or_pm = "PM"
        hours -= 12
    elif hours == 12:
        am_or_pm = "PM"

    # format minutes with leading zeros
    if mins < 10:
        mins = "0" + str(mins)

    return f"{hours}:{mins} {am_or_pm}"
