import os, random
from PIL import Image

class ImageObject:
    def __init__(self, image, offset, lHug, rHug):
        self.Image = image   # The Image
        self.Offset = offset # Push the Image Down
        self.leftHug = lHug  # Left Hug
        self.rightHug = rHug # Right Hug

def getAlphabet(a):
    specialDict = {' ': 'blank', '\\': 'backslash', ':': 'colon', '"': 'doubQu', \
                   '/': 'forwardslash', '>': 'greaterthan', '<': 'lessthan', '.': 'period', \
                   '|': 'pipe', '?': 'question', '*': 'star', '': 'thinBlank'
                   }

    [offset, lHug, rHug] = [0, 0, 0]

    offsetDict = {'y': [65, 15, 2], 'f': [20, 0, 0], 'j': [50, 0, 0], 'p': [40, 0, 0], 'g': [65, 10, 0], \
                  'F': [0, 0, 25], 'T': [0, 0, 15], 'J': [0, 0, 10], 'a': [0, 0, 5], 'b': [0, 0, 15], 'q': [50, 0, 0], \
                  'l': [0, 0, 5], 'V': [0, 0, 5], '"': [-60, 0, 0], '.': [0, -5, -5]  # ,':':[-30,0,0]
                  }
    # Assigning Offset values for chars if they exist
    if (a in offsetDict.keys()):
        [offset, lHug, rHug] = offsetDict[a]

    if (a >= 'a' and a <= 'z'):
        a = '_' + a
    path = './/FinalCharTree//' + a

    if (a in specialDict.keys()):
        path = './/FinalCharTree//__//' + specialDict[a]
        
    files = os.listdir(path)
    fileIndex = random.randrange(0,len(files))
    image = Image.open(path + '//'+ files[fileIndex])

    image_object = ImageObject(image, offset, lHug, rHug)
    
    return image_object

# The combining of any 2 images goes through this function
# Its purposes is to stitch 2 image objects perfectly(based on the indivisual offset values) and return an image object(containing residual metadata)
def stitcher(imageOb1, imageOb2): # Note: this is an order specific function

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

    # Creating A Blank Canvas, on which the images inputed will be pasted appropriately
    new_image = Image.new('RGBA', # Image has R G B and an alpha channel
                          (image1_size[0] + image2_size[0] - image1_RH - image2_LH,
                                maxHeight + maxOffset), # Dimensions calculations
                          (250, 250, 250, 0)) # Trasnparent Canvas

    new_image.paste(image1, (0, maxHeight - image1_height))

    #print(image1_RH)

    new_image.paste(image2, (image1_size[0] - image1_RH - image2_LH,
                             maxHeight - image2_height),
                    image2)

    new_image.paste(image2, (image1_size[0] - image1_RH - image2_LH,
                             maxHeight - image2_height),
                    image2)

    result = ImageObject(new_image, maxOffset, 0, image2_RH)

    return result


def wordSmith(word):
    if(len(word)< 2):
        image = getAlphabet(word)
    else:
        baseImage = getAlphabet(word[0])
        for i in range(1, len(word)):
            extention = getAlphabet(word[i])
            baseImage = stitcher(baseImage, extention)
        image = baseImage
    return image

def intialConversions(img):
    pixdata = img.load()

    # Grid Image Dimensions
    width, height = img.size

    # Converting White Spaces To Transparent Pixels
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):  # White turns too
                pixdata[x, y] = (255, 255, 255, 0)  # Transparent

    # Converting Non Transparent Spaces to Black Pixels
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] != (255, 255, 255, 0):  # Non Transparent turns too
                pixdata[x, y] = (0, 0, 0, 255)  # Black


## Genertaing a Grid of Slicing Lines
def grider(image):
    width, height = image.size
    pixdata = image.load()

    # Checks if a particular row/ column is has a certain threshold of black pixels
    def someBlack(image, xCheck, yCheck):  # Returns True/ False
        result = False
        countPix = 0
        maxPix = 10  # The Threshold

        pixdata = image.load()

        if (yCheck == None):
            for y in range(height):
                # print(picdata[xCheck, y])
                if (pixdata[xCheck, y][3] != 0):
                    # print('SomeBlack')
                    countPix += 1
                    if (countPix > maxPix):
                        # print(countPix)
                        result = True
                        break

        if (xCheck == None):
            for x in range(width):
                if (pixdata[x, yCheck][3] != 0):
                    countPix += 1
                    if (countPix > maxPix):
                        # print(countPix)
                        result = True
                        break

        return result

    # Checks if a particular row/ column is completely transparent
    def totalClear(image, xCheck, yCheck):  # Returns True/ False
        result = True
        pixdata = image.load()

        if (yCheck == None):
            for y in range(height):
                if (pixdata[xCheck, y][3] != 0):
                    result = False
                    break

        if (xCheck == None):
            for x in range(width):
                if (pixdata[x, yCheck][3] != 0):
                    result = False
                    break

        #         if (result):
        #             print('TOTal clear')
        return result

    # List that stores the x/y slicing lines
    xLines = []
    yLines = []

    # Defines the conditon whether or not be are looking for a slicing line or not
    looking = False

    # Computing The Vertical Slicing Lines
    for x in range(width):
        if (looking == False):
            if (someBlack(image, x, None)):
                # print(x)
                looking = True

        if (looking == True):
            if (totalClear(image, x, None)):
                xLines.append(x)
                looking = False

    # Resets for Horizontal
    looking = False

    # Computing The Horizontal Slicing Lines
    for y in range(height):
        if (looking == False):
            if (someBlack(image, None, y)):
                # print("SomeBlack- " + str(y))
                looking = True

        if (looking == True):
            if (totalClear(image, None, y)):
                # print('Trans- '+ str(y))
                yLines.append(y)
                looking = False

    # print(xLines, yLines)
    return [xLines, yLines] 


# Drawing the grid
# This purely for display purposes
# To check if the slices are accurate
def DrawGrid(img, slicingLines):
    horLine = Image.open('horLine.png')
    vertLine = Image.open('vertLine.png')

    gridDemo = img.copy()

    for i in slicingLines[0]:
        for j in slicingLines[1]:
            gridDemo.paste(vertLine, (i , 0))
            gridDemo.paste(horLine, (0 , j))

    # gridDemo.show()
    return gridDemo


## Cropping The Images Base on the Grid
def cropper(img, xyLines):
    width, height = img.size

    [left, right, top, bottom] = [[], [], [], []]

    # Generating Lists To Pull From To Crop
    left = xyLines[0].copy()
    right = left.copy()

    left.insert(0, 0)
    right.append(width)

    top = xyLines[1].copy()
    bottom = top.copy()

    top.insert(0, 0)
    bottom.append(height)

    # Storing the cropped images based directly off the grid
    croppedImages = []

    # print(len(top) * len(left)) #Number of images

    # The loop that crops and store the images off the grid
    for rowIndex in range(len(top)):
        for columnIndex in range(len(left)):
            # xSize = right[columnIndex] - left[columnIndex]
            # ySize = bottom[rowIndex] - top[rowIndex]

            # print((left[columnIndex], top[rowIndex], xSize, ySize))

            crop = img.crop(
                (left[columnIndex], top[rowIndex], right[columnIndex], bottom[rowIndex]))  # , xSize, ySize))
            croppedImages.append(crop)

    print(len(croppedImages))
    # Stores all the NonBlank Images
    nonBlanks = []

    # Returns False if image in blank
    def nonBlank(img):
        width, height = img.size
        pixdata = img.load()

        result = False

        for y in range(height):
            for x in range(width):
                if (pixdata[x, y][3] != 0):  # Black
                    result = True
                    break
        return result

    # Takes in an image and takes out all the extra blank space of the image
    def zealousCrop(input_image):
        def totalClear(image, xCheck, yCheck):
            width, height = image.size
            # print(width, height)
            pixdata = image.load()
            result = True
            if (yCheck == None):
                for y in range(height):
                    if (pixdata[xCheck, y][3] != 0):  # Transparent
                        result = False
                        break
            if (xCheck == None):
                for x in range(width):

                    if (pixdata[x, yCheck][3] != 0):
                        result = False
                        break
            return result

        image = input_image.copy()

        # Shaving the top
        # print("TOP")
        while (totalClear(image, None, 0)):
            width, height = image.size

            image = image.crop((0, 1, width, height))

        # Shaving Bottom
        # print("BOTTOM")
        width, height = image.size
        while (totalClear(image, None, height - 1)):
            image = image.crop((0, 0, width, height - 1))
            width, height = image.size

        # Shaving Left
        # print("LEFT")
        while (totalClear(image, 0, None)):
            width, height = image.size

            image = image.crop((1, 0, width, height))

        # print("RIGHT")
        width, height = image.size
        while (totalClear(image, width - 1, None)):
            image = image.crop((0, 0, width - 1, height))
            width, height = image.size

        return image

    # Removing Empty Images
    for i in croppedImages:
        if ((nonBlank(i))):
            nonBlanks.append(i)

    print(len(nonBlanks))

    zealousCropped = []

    # AutoCroping the Images
    for i in nonBlanks:
        zealousCropped.append(zealousCrop(i))

    finalImages = zealousCropped
    return finalImages

# Auto Sorting  into A char tree
def AutoSorter(slicedImages, sampleNumber, charOrder):
    # The number of samples of each char

    # The order of the chars
    # charOrder = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789:;-+/\*()[]{}@|#$<>%&=^"
    #charOrder = """~.,'"!?"""

    nameCharTree = "FinalCharTree"

    def makePath(path):
        if not os.path.isdir(path):
            os.makedirs(path)

    treePath = './/' + nameCharTree

    makePath(treePath)

    specialDict = {' ': 'blank', '\\': 'backslash', ':': 'colon', '"': 'doubQu',
                   '/': 'forwardslash', '>': 'greaterthan', '<': 'lessthan', '.': 'period',
                   '|': 'pipe', '?': 'question', '*': 'star', '': 'thinBlank'
                   }

    for charIndex in range(len(charOrder)):
        char = charOrder[charIndex]
        print(char)
        if (char >= 'a' and char <= 'z'):
            pathExt = '//_' + char

        elif (char in specialDict.keys()):
            pathExt = '//__//' + specialDict[char]

        else:
            pathExt = '//' + char

        path = treePath + pathExt
        print(path)
        makePath(path)
        for imageIndex in range(10):
            image = slicedImages[(10 * charIndex):(10 * charIndex) + sampleNumber][imageIndex]
            image.save(path + '//' + str(imageIndex) + '.png', format="png")

