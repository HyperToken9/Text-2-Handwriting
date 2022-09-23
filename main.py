import os
import sys
import time

import HandwritingFunctions


def main():
    # Getting .txt File Path
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("No CMLArgs Found\nEnter Path To .txt File: ")

    with open(file_path) as f:
        text = f.readlines()

    # Assigning Project Name
    project_name = input("Enter Project Name (Skip with ENTER): ")

    if project_name == '':
        project_name = "output_" + str(os.getpid())
        print("Set To Default")

    stamp = ''  # input("Enter a Tag you would like to add to the top of each page")

    # if stamp == '':
    #     stamp = """Name: Nathan Adrian Saldanha
    #     Reg. No.: 1234567
    #     Branch: CSE
    #     """

    [need_stamp, need_pdf, need_images] = [True, True, True]

    HandwritingFunctions.WritePages(project_name, text, stamp, [need_stamp, need_pdf, need_images])


if __name__ == '__main__':
    start_time = time.perf_counter()

    main()

    print("Took ", time.perf_counter() - start_time, "seconds to write")
