import os

from dotenv import load_dotenv

if __name__ == "__main__":
    print("Hello world :) :)")
    load_dotenv()
    print(os.environ["MY_VAR"])
