from teacher_data import teachers, timetable


def calculate_score(teacher, cls):

    score = 0

    # Same subject
    if teacher["subject"] == cls["subject"]:
        score += 50

    # Specialization match
    if cls["class"] in teacher["specialization"]:
        score += 30

    # Free slot
    if cls["period"] in teacher["freeSlots"]:
        score += 20

    # Lower workload preferred
    score += (10 - teacher["currentLoad"])

    return score


def assign_replacement(absent_teacher):

    replacements = []

    for cls in timetable:

        if cls["teacher"].lower() == absent_teacher.lower():

            candidates = []

            # NORMAL AI SEARCH
            for teacher in teachers:

                if teacher["name"].lower() == absent_teacher.lower():
                    continue

                score = calculate_score(teacher, cls)

                candidates.append({
                    "teacher": teacher,
                    "score": score
                })

            # SORT BEST MATCH
            candidates.sort(
                key=lambda x: x["score"],
                reverse=True
            )

            # AI FOUND MATCH
            if candidates:

                best_teacher = candidates[0]["teacher"]

                # Decide mode
                if cls["period"] in best_teacher["freeSlots"]:

                    mode = "AI Optimized Replacement"

                else:

                    mode = "Emergency Slot Adjustment"

                replacements.append({

                    "section": cls["section"],
                    "class": cls["class"],
                    "subject": cls["subject"],
                    "replacementTeacher": best_teacher["name"],
                    "aiScore": candidates[0]["score"],
                    "mode": mode

                })

                # Increase workload
                best_teacher["currentLoad"] += 1

            # LAST RESORT
            else:

                emergency_teacher = min(
                    teachers,
                    key=lambda x: x["currentLoad"]
                )

                replacements.append({

                    "section": cls["section"],
                    "class": cls["class"],
                    "subject": cls["subject"],
                    "replacementTeacher": emergency_teacher["name"],
                    "aiScore": 0,
                    "mode": "Emergency Assignment"

                })

    return replacements