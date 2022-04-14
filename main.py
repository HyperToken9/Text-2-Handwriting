from PIL import Image
import os, random, pickle, time


## Creating A Image Object That Can Hold Meta Data For Each Char
class ImageObject:

    def __init__(self, image, offset, lHug, rHug):
        # the image itself
        self.Image = image

        # how many pixels does the char need to be pushed down
        self.Offset = offset

        # how many pixels does the char need to be pushed toward the left ( in order to hug the neighbouring chars better)
        self.leftHug = lHug

        # how many pixels does the char need to be pushed toward the right ( in  order to hug the neighbouring chars better)
        self.rightHug = rHug


# Ever Char Request Goes Through This Function


# The objective of this function:
# When asked for a particular char, it searches for that char's path in the CHARTREE, picks one image randomly
# Checks of that char has any offset values and returns an Image Object
def getAlphabet(a):
    # print(a)
    # Dictionary of characters that windows doesnot allow to be used as folder names
    specialDict = {' ': 'blank', '\\': 'backslash', ':': 'colon', '"': 'doubQu',
                   '/': 'forwardslash', '>': 'greaterthan', '<': 'lessthan', '.': 'period',
                   '|': 'pipe', '?': 'question', '*': 'star', '': 'thinBlank'
                   }

    # Default meta data for an image object is a null 3 dimensional matrix
    [offset, lHug, rHug] = [0, 0, 0]

    # Dictionary containing standard offset values for each char
    offsetDict = {'y': [75, 10, 2], 'f': [20, 0, 0], 'j': [50, 0, 0], 'p': [33, 0, 0], 'g': [70, 10, 0],
                  'F': [0, 0, 10], 'T': [0, 0, 20], 'J': [0, 0, 10], 'a': [0, 0, 5], 'b': [0, 0, 5],
                  'q': [65, 0, 0], 'l': [0, 0, 5], 'V': [0, 0, 5], '"': [-60, 0, 0], '.': [0, -5, -5],
                  'n': [0, 5, 0], 'e': [0, 0, 3], ',': [10, 0, 0], '-': [-33, -2, -3], "'": [-60, 0, 0]
                  }

    # Assigning Offset values for chars if they exist
    if (a in offsetDict.keys()):
        [offset, lHug, rHug] = offsetDict[a]

    # Determining the path where the images of the char are stored depending on the value of the char
    if (a >= 'a' and a <= 'z'):
        a = '_' + a

    path = './/' + charTree + '//' + a

    if (a in specialDict.keys()):
        path = './/' + charTree + '//__//' + specialDict[a]

    # List of all the images at that destination
    files = os.listdir(path)

    # If the location has any images
    if (len(files) != 0):

        # we choose one randomly
        fileIndex = random.randrange(0, len(files))

        # this image will be returned as part of our image object
        image = Image.open(path + '//' + files[fileIndex])

    # If the location is empty
    else:
        # I have a big red box to highlight errors
        path = './/' + charTree + '//__//ERROR//ERROR.png'
        image = Image.open(path)

    # Now with an image of the char and its respective offset values we can prep our image object and return it
    result = ImageObject(image, offset, lHug, rHug)

    return result


# The combining of any 2 images goes through this function
# Its purposes is to stitch 2 image objects perfectly(based on the indivisual offset values) and return an image object(containing residual metadata)
def stitcher(imageOb1, imageOb2):  # Note: this is an order specific function

    # The Images
    image1 = imageOb1.Image
    image2 = imageOb2.Image

    # Convert Images to RGBA
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    # The Offsets of The Images
    image1_offset = imageOb1.Offset
    image2_offset = imageOb2.Offset

    # Left Hug of the 2nd Image
    image2_LH = imageOb2.leftHug

    # Right Hug of the 1st Image
    image1_RH = imageOb1.rightHug

    ## The above 2 metadata are the only ones relevant to generate the stitched image

    # The right hug of the 2nd image is out residual metadat which is returned as part of the final image object
    image2_RH = imageOb2.rightHug

    # NOTE: The left hug of the 1st image is discarded

    # The Dimensions of The Images
    image1_size = image1.size
    image2_size = image2.size

    # The Heights of The Images(as calculated above the RestingLine)
    image1_height = image1_size[1] - image1_offset
    image2_height = image2_size[1] - image2_offset

    # Parameters for dimensions of blank canvas
    maxOffset = max(image1_offset, image2_offset)
    maxHeight = max(image1_height, image2_height)

    # height = max(image1_size[1]- image1_offset, image2_size[1]- image2_offset)

    # Creating A Blank Canvas, on which the images inputed will be pasted appropriately
    new_image = Image.new('RGBA',  # Image has R G B and an alpha channel
                          (image1_size[0] + image2_size[0] - image1_RH - image2_LH, maxHeight + maxOffset),
                          # Dimensions calculations
                          (250, 250, 250, 0))  # Trasnparent Canvas

    new_image.paste(image1, (0, maxHeight - image1_height))

    new_image.paste(image2, (image1_size[0] - image1_RH - image2_LH, maxHeight - image2_height), image2)
    new_image.paste(image2, (image1_size[0] - image1_RH - image2_LH, maxHeight - image2_height), image2)

    result = ImageObject(new_image, maxOffset, 0, image2_RH)

    return result


# wordSmith Orchastrates the fetching and stitching of a Line
def wordSmith(word):
    print(word)
    if (len(word) < 2):
        base_imageObj = getAlphabet(word)

    else:
        base_imageObj = getAlphabet(word[0])
        for i in range(1, len(word)):
            base_imageObj = stitcher(base_imageObj, getAlphabet(word[i]))

    return base_imageObj


def resize(image, percentageChangeX, percentageChangeY):
    # Getting OG Size
    imageSizeX = image.size[0]
    imageSizeY = image.size[1]

    # Calculating New Size
    newSizeX = (imageSizeX * percentageChangeX) / 100
    newSizeY = (imageSizeY * percentageChangeY) / 100

    # Resizing
    new_image = image.resize((int(newSizeX), int(newSizeY)))

    return new_image


def lineSize(line):
    length = 0
    for i in line:
        # print(i)
        length += size_dict[i]
    return length


# Takes in The text and gives an list of pages
def formater(projectName, Text, stamp, optionality):
    # Tries to remove unnessasary chars
    def cleanerUpper(text):
        newText = ''
        for i in range(len(text)):
            if (text[i] in '“”'):# double quote
                a = '"'
            elif (text[i] in "’’’‘"):# single quote
                a = "'"
            elif (text[i] == '—' or text[i] == '–'): # hyphen
                a = '-'
            elif (text[i] == '…'):# elipses
                a = '...'
            else:
                a = text[i]
            newText += a

        newTextSplit = newText.split('\n')

        while (newTextSplit[-1] == ''):
            newTextSplit = newTextSplit[:-1]

        separator = '\n'
        # Getting Rid Of empty paras at the end
        newText = separator.join(newTextSplit)

        return (newText)

    ##TODO: There can be a function that lines down the next page while the prev. page is being pasted
    pages = []

    def WriteThePage(List):

        # Getting A Page
        path = './/Papers//' + PageAlignment
        files = os.listdir(path)
        fileIndex = random.randrange(0, len(files))
        # print(path+'//'+files[fileIndex])
        pageImage = Image.open(path + '//' + files[fileIndex])

        # Setting Up The Page
        new_image = Image.new('RGBA', (pageImage.size), (250, 250, 250, 0))
        new_image.paste(pageImage, (0, 0))

        # Printing Each Line At Alloted Line Number
        for line in List:
            lineOffset = line[1].Offset
            lineImage = line[1].Image
            currentLineNumber = line[0]
            # Randomize the start position from (400-450)
            imageHeight = lineImage.size[1] - lineOffset

            yCoord = 412 + (103 * currentLineNumber) - (imageHeight)
            # print(yCoord)
            variableStart = random.randint(0, 20)
            new_image.paste(lineImage, (395 + variableStart, yCoord), mask=lineImage)
            # new_image.show()

        pages.append(new_image)

    # Clean the text off unusual characters
    Text = cleanerUpper(Text)

    PageAlignment = 'Left'

    # Active Line Writing To
    lineNumber = 0

    paraList = Text.split('\n')

    line = ''
    lineList = []
    print('Generating Page 1')

    for paraIndex in range(len(paraList)):
        para = paraList[paraIndex]
        if (para == ''):
            lineNumber += 1
            if (lineNumber > 27):
                WriteThePage(lineList)
                lineList = []
                lineNumber = 0

        for charIndex in range(len(para)):
            line += para[charIndex]
            # lineImageObject = wordSmith(line)
            # lineImage = lineImageObject.Image

            lineLength = lineSize(line)

            maxLineSize = 2150

            if (lineLength > maxLineSize or charIndex == len(para) - 1):
                if (lineLength > maxLineSize):
                    oldLine = line
                    while line[-1] != ' ':
                        line = line[:-1]
                    snippedOff = oldLine[len(line):]
                else:
                    # print("end :" + para[-10:charIndex+1])
                    snippedOff = ''

                if (lineNumber > 27):
                    print("Printing Page " + str(len(pages) + 1))
                    WriteThePage(lineList)

                    print('Generating Page ' + str(len(pages) + 1))
                    lineList = []
                    lineNumber = 0

                finalLineImageObject = wordSmith(line)
                lineList.append([lineNumber, finalLineImageObject])
                lineNumber += 1
                print(str(int((lineNumber / 28) * 100)) + '%')
                line = snippedOff

                if ((paraIndex == (len(paraList) - 1)) and charIndex == len(para) - 1):
                    WriteThePage(lineList)
                    lineList = []
                    lineNumber = 0

                # or

    def stamper(pages, stamp):

        def generateStamp(stamp):
            lines = stamp.split('\n')
            numLines = len(lines)
            canvas = None

            lineSeparation = random.randint(90, 100)
            for lineIndex in range(numLines):
                if (canvas == None):
                    canvas = wordSmith(lines[lineIndex]).Image
                else:
                    canvasExt = wordSmith(lines[lineIndex]).Image
                    canvasSize = canvas.size
                    canvasExtSize = canvasExt.size
                    tilt = random.randint(0, 10)
                    newCanvas = Image.new('RGBA',
                                          (max(canvasSize[0], canvasExtSize[0]) + tilt,
                                           canvasSize[1] + canvasExtSize[1]),
                                          (250, 250, 250, 0))
                    newCanvas.paste(canvas, (0, 0))
                    newCanvas.paste(canvasExt, (tilt, lineIndex * lineSeparation), canvasExt)
                    newCanvas.paste(canvasExt, (tilt, lineIndex * lineSeparation), canvasExt)
                    canvas = newCanvas
            return canvas

        for pageIndex in range(len(pages)):
            page = pages[pageIndex]
            stampImage = resize(generateStamp(stamp), 80, 80)
            stampSize = stampImage.size
            pageSize = page.size
            randStartX = random.randint(25, 80)
            randStartY = random.randint(2, 20)
            page.paste(stampImage, (pageSize[0] - stampSize[0] - randStartX, randStartY), stampImage)

        return pages

    if (optionality[0]):
        pages = stamper(pages, stamp)

    def cutter(pages):
        newPages = []
        for pageIndex in range(len(pages)):
            page = pages[pageIndex]

            xCrop = random.randint(0, 150)
            yCrop = random.randint(0, 33)
            # print(page.size)
            page = page.crop((xCrop, 0, page.size[0], (page.size[1]) - yCrop))
            # print(page.size)
            newPages.append(page)
        return newPages

    pages = cutter(pages)

    def documenter(assignmentName, pages, needPDF, needImages):
        for p in range(len(pages)):
            # TODO: Maybe randomize the scaling ratios

            pages[p] = resize(pages[p].convert('RGB'), 25, 25)

        if (pages == []):
            print("No Pages To Print")
        else:
            if (needImages):
                path = './/' + assignmentName
                if not os.path.isdir(path):
                    os.makedirs(path)

                for pageIndex in range(len(pages)):
                    print('Saving... Page ' + str(pageIndex + 1))
                    page = pages[pageIndex]
                    page.save('.//' + assignmentName + '//' + str(pageIndex) + '.jpg')

            if (needPDF):
                pages[0].convert('RGB').save('.//' + assignmentName + '//' + 'myPDF.pdf', save_all=True,
                                             append_images=pages[1:])

    documenter(projectName, pages, optionality[1], optionality[2])


def main():
    projectName = "Exercise1"

    stamp = """Name: Nathan Adrian Saldanha
Reg. No.: abbacadaba
Branch: CSE
"""

    text = """"""

    if (text == ''):
        # Open File
        text_file = open('.//' + projectName + '.txt', "r",  encoding="utf-8-sig")

        # Read Text
        text = text_file.read()[:]

        # Close File
        text_file.close()

    # TODO: Ability to Pull text from text file
    needStamp = True
    needPDF = True
    needImages = True

    optionality = [needStamp, needPDF, needImages]
    print(text)
    formater(projectName, text, stamp, optionality)


if (__name__ == '__main__'):
    start_time = time.time()
    with open('.//CleanCharTree//WIDTHS.pickle', 'rb') as handle:
        size_dict = pickle.load(handle)
    print(len(size_dict.keys()))
    charTree = "CleanCharTree"
    main()
    print("My program took", time.time() - start_time, "to run")
