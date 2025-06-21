def get_exercises(responses):
    recs = []
    if responses.get("balance"):
        recs.append({"name": "Chair Marches", "description": "Improves balance", "youtube": "https://youtu.be/6oL2sy-il6Y"})
    if responses.get("joint_pain"):
        recs.append({"name": "Wall Push-Ups", "description": "Low-impact strength", "youtube": "https://youtu.be/0KNAwCGGzIE"})
    if responses.get("walk_time", 0) < 15:
        recs.append({"name": "Seated Toe Taps", "description": "Light cardio", "youtube": "https://youtu.be/UvVZHLi4Gz0"})
    if responses.get("activity") == "Low":
        recs.append({"name": "Arm Circles", "description": "Boosts shoulder mobility", "youtube": "https://youtu.be/nq0N_j2XMQw"})
    if "goal" in responses and "strength" in responses["goal"].lower():
        recs.append({"name": "Sit-to-Stand", "description": "Leg strength & control", "youtube": "https://youtu.be/o1ZLcg9Y_Do"})
    return recs
