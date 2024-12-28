import yaml
import helper

sample = "Hello World"
with open("Hello World.txt", "w") as f:
    f.write(str(sample))

helper.stop_project()