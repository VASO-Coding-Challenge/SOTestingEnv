"""This script generates a blank questions directories for the test"""

import os
import argparse


def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(
        description="Generate blank questions directories for the test"
    )
    parser.add_argument(
        "amt", type=int, default=3, help="The amount of questions to generate"
    )
    args = parser.parse_args()

    os.chdir("/workspaces/SOTestingEnv/")

    # Create the es_files directory if it doesn't exist (It should, but just in case...)
    try:
        os.chdir("es_files/")
    except:
        os.mkdir("es_files/")
        os.chdir("es_files/")

    # Create the questions directory if it doesn't exist
    try:
        os.chdir("questions/")
    except:
        os.mkdir("questions/")
        os.chdir("questions/")

    # Find the highest existing question number from the directories
    question_num = 0
    for dir in os.listdir():
        if os.path.isdir(dir):
            if int(dir[-1]) > question_num:
                question_num = int(dir[-1])

    # Generate the new directories
    for i in range(question_num, args.amt + question_num):
        generateQuestion(i + 1)


def generateQuestion(question_num: int):
    """Generates a blank question directory for the test"""
    # Generate the new directories
    os.mkdir(f"q{question_num}")
    os.chdir(f"q{question_num}")
    # Write prompt file
    with open("prompt.md", "w") as f:
        f.write(f"Template prompt for question {question_num}")
    # Write the test.py file
    with open("test_cases.py", "w") as f:
        f.write(
            f'"""Template testing code for question {question_num}. This is for final results tallying."""'
            "\n\ndef test():\n    pass\n"
        )
    # Write the test.py file
    with open("demo_cases.py", "w") as f:
        f.write(
            f'"""Template demo testing code for question {question_num}. This is for student submission trial and error."""'
            "\n\ndef demo():\n    pass\n"
        )
    # Go back to the questions directory
    os.chdir("..")


if __name__ == "__main__":
    main()
