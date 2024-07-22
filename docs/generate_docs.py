import os

def generate_autodoc():
    os.system('sphinx-apidoc -o source/ ../frame')

if __name__ == "__main__":
    generate_autodoc()
