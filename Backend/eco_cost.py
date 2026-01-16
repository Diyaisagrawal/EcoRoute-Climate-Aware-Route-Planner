# def aqi_penalty(aqi):
#     if aqi <= 50: return 0
#     if aqi <= 100: return 1
#     if aqi <= 150: return 3
#     if aqi <= 200: return 6
#     return 10


# def temp_penalty(temp):
#     if 18 <= temp <= 30:
#         return 0
#     return abs(temp - 24) * 0.2
def eco_penalty(aqi, temp):
    aqi_cost = 0
    if aqi > 50: aqi_cost = (aqi - 50) * 0.02

    temp_cost = abs(temp - 24) * 0.05

    return aqi_cost + temp_cost
