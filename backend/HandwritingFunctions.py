import os
import pickle
import random

from PIL import Image

current_file_path = os.path.abspath(__file__)
base_directory = os.path.dirname(current_file_path)
print(base_directory)

tree_name = 'Character Tree'
resource_folder = 'Resources'
tree_path = os.path.join(base_directory, resource_folder, tree_name)



# Hold Meta Data For Each Character's Image
class ImageObject:

    def __init__(self, image, offset, left_hug, right_hug):
        # the image itself
        self.Image = image

        # how many pixels does the char need to be pushed down
        self.Offset = offset

        # how many pixels does the char need to be pushed toward the left
        self.leftHug = left_hug

        # how many pixels does the char need to be pushed toward the right
        self.rightHug = right_hug

    # Stitches 2 Images Together
    def __add__(self, img_obj):
        # The Images
        image1 = self.Image
        image2 = img_obj.Image

        # Convert Images to RGBA
        image1 = image1.convert("RGBA")
        image2 = image2.convert("RGBA")

        # The Offsets of The Images
        image1_offset = self.Offset
        image2_offset = img_obj.Offset

        # Left Hug of the 2nd Image
        image2_lh = img_obj.leftHug

        # Right Hug of the 1st Image
        image1_rh = self.rightHug

        # The above 2 metadata are the only ones relevant to generate the stitched image

        # The right hug of the 2nd image is out residual metadata which is returned as part of the final image object
        image2_rh = img_obj.rightHug

        # NOTE: The left hug of the 1st image is discarded

        # The Dimensions of The Images
        image1_size = image1.size
        image2_size = image2.size

        # The Heights of The Images(as calculated above the RestingLine)
        image1_height = image1_size[1] - image1_offset
        image2_height = image2_size[1] - image2_offset

        # Parameters for dimensions of blank canvas
        max_offset = max(image1_offset, image2_offset)
        max_height = max(image1_height, image2_height)

        # Creating A Blank Canvas, on which the images inputted will be pasted appropriately
        new_image = Image.new('RGBA',  # Image has R G B and an alpha channel
                              (image1_size[0] + image2_size[0] - image1_rh - image2_lh, max_height + max_offset),
                              # Dimensions calculations
                              (250, 250, 250, 0))  # Transparent Canvas

        new_image.paste(image1, (0, max_height - image1_height))

        new_image.paste(image2, (image1_size[0] - image1_rh - image2_lh, max_height - image2_height), image2)
        new_image.paste(image2, (image1_size[0] - image1_rh - image2_lh, max_height - image2_height), image2)

        result = ImageObject(new_image, max_offset, 0, image2_rh)

        return result


# Dictionary to cache ImageObjects
image_cache = {}

class WriteLine:

    def __init__(self, line):
        # print('Line ',line)
        self.line_content = line

    # Fetches Character Image From Directory
    @staticmethod
    def getAlphabet(a):

        global tree_path

        # print(a)
        # Dictionary of characters that windows doesn't allow to be used as folder names
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
        if a in offsetDict.keys():
            [offset, lHug, rHug] = offsetDict[a]

        # Determining the path where the images of the char are stored depending on the value of the char
        if 'a' <= a <= 'z':
            a = '_' + a

        path = os.path.join(tree_path, a) 

        if a in specialDict.keys():
            path = os.path.join(tree_path, '__', specialDict[a]) 

        if path in image_cache.keys():
            fileIndex = random.randrange(0, len(image_cache[path]))
            image = image_cache[path][fileIndex]
            return ImageObject(image, offset, lHug, rHug)

        # List of all the images at that destination
        files = os.listdir(path)

        # If the location has any images
        if len(files) != 0:

            # we choose one randomly
            fileIndex = random.randrange(0, len(files))

            local_char_cache = []

            for file in files:
                local_char_cache.append(Image.open(os.path.join(path, file)))

            image_cache[path] = local_char_cache
            # this image will be returned as part of our image object
            # image = Image.open(os.path.join(path, files[fileIndex]))
            image = local_char_cache[fileIndex]



        # If the location is empty
        else:
            # I have a big red box to highlight errors
            path = os.path.join(tree_path, '__', 'ERROR', 'ERROR.png')
            image = Image.open(path)

        # Now with an image of the char and its respective offset values we can prep our image object and return it
        result = ImageObject(image, offset, lHug, rHug)

        return result

    # Generates A Full Sentence
    def generate_line(self):

        word = self.line_content

        # print('Word ',word)

        if len(word) < 2:
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


def resize(image, percentage_change_x, percentage_change_y):
    # Getting OG Size
    imageSizeX = image.size[0]
    imageSizeY = image.size[1]

    # Calculating New Size
    newSizeX = (imageSizeX * percentage_change_x) / 100
    newSizeY = (imageSizeY * percentage_change_y) / 100

    # Resizing
    new_image = image.resize((int(newSizeX), int(newSizeY)))

    return new_image


with open(os.path.join(tree_path, "WIDTHS.pickle"), 'rb') as handle:
    size_dict = pickle.load(handle)


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


class WritePages:

    def __init__(self, project_name, content, stamp, options):

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
            if text[i] in '“”':  # double quote
                a = '"'
            elif text[i] in "’’’‘":  # single quote
                a = "'"
            elif text[i] in '—–':  # hyphen
                a = '-'
            elif text[i] == '…':  # ellipses
                a = '...'
            else:
                a = text[i]
            new_text += a

        newTextSplit = new_text.split('\n')

        while newTextSplit[-1] == '':
            newTextSplit = newTextSplit[:-1]

        separator = '\n'
        # Getting Rid Of empty paras at the end
        new_text = separator.join(newTextSplit)

        self.Content = new_text

    def generate_page(self, line_list):

        # Getting A Page
        path = os.path.join(base_directory, resource_folder, 'Papers', 'Pages')
        files = os.listdir(path)
        file_index = random.randrange(0, len(files))
        pageImage = Image.open(os.path.join(path, files[file_index]))

        # Setting Up The Page
        new_image = Image.new('RGBA', pageImage.size, (250, 250, 250, 0))
        new_image.paste(pageImage, (0, 0))

        # Printing Each Line At Allotted Line Number
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

        if self.Optionality[0]:
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
            if para == '':
                lineNumber += 1
                if lineNumber > 27:
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

                if lineLength > maxLineSize or charIndex == len(para) - 1:
                    if lineLength > maxLineSize:
                        oldLine = line
                        while line[-1] != ' ':
                            line = line[:-1]
                        snippedOff = oldLine[len(line):]
                    else:
                        # print("end :" + para[-10:charIndex+1])
                        snippedOff = ''

                    if lineNumber > 27:
                        print("Printing Page " + str(len(self.Pages) + 1))
                        # print('Tick 2')
                        self.generate_page(lineList)

                        print('Generating Page ' + str(len(self.Pages) + 1))
                        lineList = []
                        lineNumber = 0

                    finalLineImageObject = WriteLine(line).generate_line()
                    lineList.append([lineNumber, finalLineImageObject])
                    lineNumber += 1

                    # print(str(int((lineNumber / 28) * 100)) + '%')

                    line = snippedOff

                    if (paraIndex == (len(paraList) - 1)) and charIndex == len(para) - 1:
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
                if canvas is None:
                    # print('lines[lineIndex] ',lines[lineIndex])
                    canvas = WriteLine(lines[lineIndex]).generate_line().Image
                else:
                    canvasExt = WriteLine(lines[lineIndex]).generate_line().Image
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
        global base_directory
        pages = self.Pages

        needImages = self.Optionality[1]

        needPDF = self.Optionality[2]

        for p in range(len(pages)):
            # TODO: Maybe randomize the scaling ratios

            pages[p] = resize(pages[p].convert('RGB'), 25, 25)

        if not pages:
            print("No Pages To Print")
        else:
            if needImages:
                path = os.path.join(base_directory ,self.Project_Name)
                if not os.path.isdir(path):
                    os.makedirs(path)

                for pageIndex in range(len(pages)):
                    print('Saving... Page ' + str(pageIndex + 1))
                    page = pages[pageIndex]
                    page.save(os.path.join(base_directory, self.Project_Name, str(pageIndex) + '.jpg'))

            if needPDF:
                pages[0].convert('RGB').save(os.path.join(base_directory, self.Project_Name, self.Project_Name + '.pdf'),
                                             save_all=True,
                                             append_images=pages[1:])
