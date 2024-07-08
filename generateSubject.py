# C-Fiber Study Script Generator
# v1.1
# Author: Abdallah Sher
# Date: 2024-07-08
## This script generates Dapsys scripts for digitimer stimulator based on user input.
## The user can choose to use presets defined in the code, or input their own parameters as the script runs.
## The user also has the option to generate a random order for voltages to be administered


import os
import random

# Preset parameters for the script
def presets():
    # 10 Pulses at 0.25s duration
    preset1 = {
        "voltage":"0.05",
        "frequencies":"4",
        "duration":"0.25",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    preset2 = {
        "voltage":"0.1",
        "frequencies":"4",
        "duration":"0.25",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    preset3 = {
        "voltage":"0.2",
        "frequencies":"4",
        "duration":"0.25",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    # 10 Pulses at 2.5s duration
    preset4 = {
        "voltage":"0.05",
        "frequencies":"4",
        "duration":"2.5",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    preset5 = {
        "voltage":"0.1",
        "frequencies":"4",
        "duration":"2.5",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    preset6 = {
        "voltage":"0.2",
        "frequencies":"4",
        "duration":"2.5",
        "pulses":"10",
        "ipi":["10", "20"]
    }
    # 1 pulse at 60s duration
    preset7 = {
        "voltage":"0.05",
        "frequencies":"4",
        "duration":"60",
        "pulses":"1",
        "ipi":["10", "20"]
    }
    preset8 = {
        "voltage":"0.1",
        "frequencies":"4",
        "duration":"60",
        "pulses":"1",
        "ipi":["10", "20"]
    }
    preset9 = {
        "voltage":"0.2",
        "frequencies":"4",
        "duration":"60",
        "pulses":"1",
        "ipi":["10", "20"]
    }

    presets = [preset1, preset2, preset3, preset4, preset5, preset6, preset7, preset8, preset9]
    return presets

def createScript(filePath, scriptParam):
    voltage, frequencies, duration, pulses, ipi = scriptParam.values()
    fileName = filePath + voltage + "mA_" + frequencies + "Hz_" + duration + "s_" + pulses + "P.txt"
    pulses = int(pulses)
    ipi = [int(i) for i in ipi]
    with open(fileName, "w") as f:
        f.write("Wait(30, \"\")\n")
        for i in range(pulses):
            f.write("TTL(225,1)\n")
            f.write("Sine(" + duration + ", " + frequencies + ", " + voltage + ", 0, \"\")\n")
            interval = random.randint(ipi[0], ipi[1])
            interval = str(interval)
            f.write("Wait(" + interval + ", \"\")\n")
            f.write("TTL(225,0)\n")
    print("Script generated: " + fileName)

def defineScript():
    print("Enter the voltage to generate: ")
    voltage = input()
    print("Enter the frequency at which to generate the voltage: ")
    frequencies = input()
    print("Enter the durations you'd like to generate in seconds: ")
    duration = input()
    print("Enter the number of pulses to generate: ")
    pulses = input()
    print("Enter inclusive boundaries for inter-pulse intervals (in seconds) separated by a space: ")
    ipi = input().split()
    return {"voltage":voltage, "frequencies":frequencies, "duration":duration, "pulses":pulses, "ipi":ipi}


def generateScripts(subject):
    filePath = "Subject_Scripts/" + subject + "/"
    print("Use presets? (Y/N)")
    usePresets = True if input() == "Y" else False
    print("Randomize the order of the voltages? (Y/N)")
    randomize = True if input() == "Y" else False
    voltages = []
    if usePresets:
        presetParams = presets()
        for preset in presetParams:
            createScript(filePath, preset)
            if preset["voltage"] not in voltages:
                voltages.append(preset["voltage"])
        newScript = False
    else:
        newScript = True
    while(newScript):
        print("Beginning Script Generation...")
        scriptParam = defineScript()
        if scriptParam[0] not in voltages:
            voltages.append(scriptParam[0])
        createScript(filePath, scriptParam)
        print("Generate another script? (Y/N)")
        newScript = True if input() == "Y" else False
    if randomize:
        random.shuffle(voltages)
        with open(filePath + "order.txt", "w") as f:
            for voltage in voltages:
                f.write(voltage + "\n")
        print("Order randomized.")

newSubject = True

while(newSubject):
    print("Enter the subject identififer: ")
    subject = input()

    if not os.path.exists("Subject_Scripts/" + subject):
        os.makedirs("Subject_Scripts/" + subject)
        print("Subject folder created.")
        generateScripts(subject)
    else:
        print("Subject already exists. Replace/Append/Or leave scripts? (R/A/N)")
        replace = input()
        if replace == "R":
            os.system("rm Subject_Scripts/" + subject + "/*")
            generateScripts(subject)
        elif replace == "A":
            generateScripts(subject)
        else:
            print("Exiting...")
            exit()
    print("Continue with another subject? (Y/N)")
    newSubject = True if input() == "Y" else False