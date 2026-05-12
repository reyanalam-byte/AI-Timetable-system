from teacher_data import teachers, timetable

def assign_replacement(absent_teacher):

    replacements = []

    for cls in timetable:

        if cls["teacher"] == absent_teacher:

            for teacher in teachers:

                if (
                    teacher["subject"] == cls["subject"]
                    and cls["period"] in teacher["freeSlots"]
                    and teacher["currentLoad"] < teacher["maxLoad"]
                ):

                    replacements.append({
                        "section": cls["section"],
                        "replacementTeacher": teacher["name"]
                    })

    return replacements