import re as feeling

# So, our story begin with 5 people talking about their feelings...

people = 5
affirmation = "Je suis remplie d'une certaine joie et d'un grand bonheur!"
for person in range(people):
    if not person:
        print(affirmation)
    matchFeeling = feeling.match(".*?(bonheur).*", affirmation)
    if matchFeeling:
        if person != people-1:
            affirmation = "Moi aussi je n'ai que trop de bonheur hihi joie xxx <3"
        else:
            affirmation = "Mais quelle heureuse nouvelle! Moi de même, je suis de bonne heure hihihi ;P"
    print(affirmation)

# And all is well that ends well! They lived happily ever after.
