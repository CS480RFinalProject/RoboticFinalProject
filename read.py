with open("file.txt", "r") as f:
    result = f.read()
print(result)
if result == "stop":
    print("TRUE")