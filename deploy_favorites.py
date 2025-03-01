from vyper import compile_code

def main():
    print("Let's read in the vyper code and deploy it!")
    with open("favorites.vy") as favorites_file:
        favorites_code = favorites_file.read()
        compilation_details = compile_code(favorites_code, output_formats=["bytecode"])
        #print(compilation_details)
    

if __name__ == "__main__":
    main()