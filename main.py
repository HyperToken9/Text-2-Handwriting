import HandwritingFucntions as hf
import time

def main():

    projectName = "Exercise1"

    stamp = """Name: Nathan Adrian Saldanha
    Reg. No.: 1234567
    Branch: CSE
    """

    text = ''

    if (text == ''):
        # Open File
        text_file = open('.//' + projectName + '.txt', "r", encoding="utf-8-sig")

        # Read Text
        text = text_file.read()[:]

        # Close File
        text_file.close()

    print(text)

    optionality = [needStamp, needPDF, needImages] = [True, True, True]


    hf.Write_Pages(projectName, text, stamp , optionality)


if (__name__ == '__main__'):

    start_time = time.time()
    main()
    print("Took ", time.time() - start_time, "seconds to write")