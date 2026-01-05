from dotenv import load_dotenv
import os


if __name__ == "__main__":
	print("Hello world :) :)")
	load_dotenv()
	print(os.environ["MY_VAR"])
