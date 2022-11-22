import os
import sys

filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(filepath)

message = "\n=======================================\n" + f"{filepath} added to PATH\n" + "=======================================\n"
print(message)