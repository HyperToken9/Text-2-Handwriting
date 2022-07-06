from PIL import Image
import os, random, pickle, time

tree_name = 'Character Tree'


## Hold Meta Data For Each Character's Image
class ImageObject:

    def __init__(self, image, offset, lHug, rHug):

        global tree_name

        # the image itself
        self.Image = image

        # how many pixels does the char need to be pushed down
        self.Offset = offset

        # how many pixels does the char need to be pushed toward the left ( in order to hug the neighbouring chars better)
        self.leftHug = lHug

        # how many pixels does the char need to be pushed toward the right ( in  order to hug the neighbouring chars better)
        self.rightHug = rHug





    # Stitches 2 Images Together
    def __add__(self, newImageObj):

        # The Images
        image1 = self.Image
        image2 = newImageObj.Image

        # Convert Images to RGBA
        image1 = image1.convert("RGBA")
        image2 = image2.convert("RGBA")

        # The Offsets of The Images
        image1_offset = self.Offset
        image2_offset = newImageObj.Offset

        # Left Hug of the 2nd Image
        image2_LH = newImageObj.leftHug

        # Right Hug of the 1st Image
        image1_RH = self.rightHug

        ## The above 2 metadata are the only ones relevant to generate the stitched image

        # The right hug of the 2nd image is out residual metadat which is returned as part of the final image object
        image2_RH = newImageObj.rightHug

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

        # new_image.show()


        # self.Image = new_image
        # self.Offset = maxOffset
        # self.leftHug = 0
        # self.rightHug = 0

        result = ImageObject(new_image, maxOffset, 0, image2_RH)

        # return self

        return result

class Write_Line:

    def __init__(self, line):
        # print('Line ',line)
        self.line_content = line


    # Fetches Character Image From Directory
    def getAlphabet(self, a):

        global tree_name

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

        path = './/' + tree_name + '//' + a

        if (a in specialDict.keys()):
            path = './/' + tree_name + '//__//' + specialDict[a]

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
            path = './/' + tree_name + '//__//ERROR//ERROR.png'
            image = Image.open(path)

        # Now with an image of the char and its respective offset values we can prep our image object and return it
        result = ImageObject(image, offset, lHug, rHug)

        return result


    # Generates A Full Sentence
    def generate_line(self):

        word = self.line_content

        # print('Word ',word)

        if (len(word) < 2):
            base_imageObj = self.getAlphabet(word)

        else:
            base_imageObj = self.getAlphabet(word[0])
            # print('Base Image Obj',base_imageObj.Offset)

            for i in range(1, len(word)):

                # print(word[i])
                # print(self.getAlphabet(word[i]).rightHug)
                base_imageObj = base_imageObj + self.getAlphabet(word[i])


        # base_imageObj.Image.show()
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

with open('.//' + tree_name +'//WIDTHS.pickle', 'rb') as handle:
    size_dict = pickle.load(handle)
# print(len(size_dict.keys()))

def lineSize(line):
    global size_dict
    length = 0
    for i in line:
        # print(i)
        length += size_dict[i]
    return length

def cutter(page):
    xCrop = random.randint(0, 150)
    yCrop = random.randint(0, 33)
    # print(page.size)
    page = page.crop((xCrop, 0, page.size[0], (page.size[1]) - yCrop))

    return page

class Write_Pages:

    def __init__(self, project_name,content, stamp, options):

        self.Project_Name = project_name

        self.Content = content


        self.Stamp = stamp
        self.Optionality = options

        self.Pages = []

        self.content_formatter()

        self.write_pages()

        self.save_pages()

    # Tries to remove unnecessary chars
    def content_formatter(self):
        text = self.Content
        new_text = ''
        for i in range(len(text)):
            if (text[i] in '“”'):  # double quote
                a = '"'
            elif (text[i] in "’’’‘"):  # single quote
                a = "'"
            elif (text[i] == '—' or text[i] == '–'):  # hyphen
                a = '-'
            elif (text[i] == '…'):  # elipses
                a = '...'
            else:
                a = text[i]
            new_text += a

        newTextSplit = new_text.split('\n')

        while (newTextSplit[-1] == ''):
            newTextSplit = newTextSplit[:-1]

        separator = '\n'
        # Getting Rid Of empty paras at the end
        new_text = separator.join(newTextSplit)

        self.Content = new_text

    def generate_page(self, line_list):

        # Getting A Page
        path = './/Papers//Pages'
        files = os.listdir(path)
        file_index = random.randrange(0, len(files))
        # print(path+'//'+files[fileIndex])
        pageImage = Image.open(path + '//' + files[file_index])

        # Setting Up The Page
        new_image = Image.new('RGBA', (pageImage.size), (250, 250, 250, 0))
        new_image.paste(pageImage, (0, 0))

        # Printing Each Line At Alloted Line Number
        for line in line_list:
            lineOffset = line[1].Offset
            lineImage = line[1].Image
            current_line_number = line[0]

            # Randomize the start position from (400-450)
            image_height = lineImage.size[1] - lineOffset

            yCoord = 412 + (103 * current_line_number) - image_height
            # print(yCoord)

            variableStart = random.randint(0, 20)
            new_image.paste(lineImage, (395 + variableStart, yCoord), mask=lineImage)
            # new_image.show()

        if (self.Optionality[0]):
            new_image = self.stamper(new_image)

        new_image = cutter(new_image)

        self.Pages.append(new_image)

    def write_pages(self):

        # Active Line Writing To
        lineNumber = 0

        paraList = self.Content.split('\n')

        line = ''
        lineList = []
        print('Generating Page 1')

        for paraIndex in range(len(paraList)):
            para = paraList[paraIndex]
            if (para == ''):
                lineNumber += 1
                if (lineNumber > 27):
                    # print('Tick 1')
                    self.generate_page(lineList)
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
                        print("Printing Page " + str(len(self.Pages) + 1))
                        # print('Tick 2')
                        self.generate_page(lineList)

                        print('Generating Page ' + str(len(self.Pages) + 1))
                        lineList = []
                        lineNumber = 0

                    finalLineImageObject = Write_Line(line).generate_line()
                    lineList.append([lineNumber, finalLineImageObject])
                    lineNumber += 1

                    # print(str(int((lineNumber / 28) * 100)) + '%')

                    line = snippedOff

                    if ((paraIndex == (len(paraList) - 1)) and charIndex == len(para) - 1):
                        # print('Tick 3')
                        self.generate_page(lineList)
                        lineList = []
                        lineNumber = 0

    def stamper(self, page):

        def generateStamp(stamp):
            lines = stamp.split('\n')
            numLines = len(lines)
            canvas = None

            lineSeparation = random.randint(90, 100)
            for lineIndex in range(numLines):
                if (canvas == None):
                    # print('lines[lineIndex] ',lines[lineIndex])
                    canvas = Write_Line(lines[lineIndex]).generate_line().Image
                else:
                    canvasExt = Write_Line(lines[lineIndex]).generate_line().Image
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

        stampImage = resize(generateStamp(self.Stamp), 80, 80)
        stampSize = stampImage.size
        pageSize = page.size
        randStartX = random.randint(25, 80)
        randStartY = random.randint(2, 20)
        page.paste(stampImage, (pageSize[0] - stampSize[0] - randStartX, randStartY), stampImage)

        return page

    def save_pages(self):

        pages = self.Pages

        needImages = self.Optionality[1]

        needPDF = self.Optionality[2]

        for p in range(len(pages)):
            # TODO: Maybe randomize the scaling ratios

            pages[p] = resize(pages[p].convert('RGB'), 25, 25)

        if (pages == []):
            print("No Pages To Print")
        else:
            if (needImages):
                path = './/' + self.Project_Name
                if not os.path.isdir(path):
                    os.makedirs(path)

                for pageIndex in range(len(pages)):
                    print('Saving... Page ' + str(pageIndex + 1))
                    page = pages[pageIndex]
                    page.save('.//' + self.Project_Name + '//' + str(pageIndex) + '.jpg')

            if (needPDF):
                pages[0].convert('RGB').save('.//' + self.Project_Name + '//' + 'myPDF.pdf', save_all=True,
                                             append_images=pages[1:])

