class Profile():
    def __init__(self, weight, height):
        self.weight = weight
        self.height = height

def create_object():
    name = input("What's your name?")
    new_weight = input("What's your height?")
    new_height = input("What's your weight?")

    name = Profile(new_weight, new_height)
    return name