from PIL import Image
import argparse


#rgb to hex
def rtoh(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

#hex to rgb
def htor(hex):
    ##removes the # in the front
    return int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:7], 16)

#string to binary
def stob(st):
    binary = bin(int.from_bytes(st.encode(), 'big'))
    #removes the 0x
    return binary[2:]

#binary to string
def btos(binary):
    #converts string to integer
    binary = int(binary, 2)
    return binary.to_bytes((binary.bit_length() + 7) // 8, 'big').decode()





#methods to encode msg last bit of hex number if its 0 or 1
def encode(hex, digit):

    if hex[-1] in ('0', '1'):
        hex = hex[:-1] + digit

        return hex
    else:
        return None


def hide(file, msg):
    img = Image.open(file)
    #message to hide in binary
    binaryMsg = stob(msg) + '11111110'#delimiter
    #tuples of rgba values Ex:(0,0,0,255)
    rgba = img.getdata()

    #list of new rgba value
    newRGBA = []
    #binary message counter
    bmCounter = 0
    temp = ''
    for item in rgba:
        if (bmCounter < len(binaryMsg)):
            newRGB = encode(rtoh(item[0], item[1], item[2]), binaryMsg[bmCounter])
            if newRGB == None:
                newRGBA.append(item)
            else:
                r, g, b = htor(newRGB)
                newRGBA.append((r, g, b, 255))
                bmCounter += 1
        else:
            newRGBA.append(item)
    img.putdata(newRGBA)
    img.save(file, "PNG")
    return "Message has been encoded into PNG."


##gets lsb if it is 0 or 1
def decode(hex):
    if hex[-1] in ('0', '1'):
        return hex[-1]
    else:
        return None


def reveal(file):
    img = Image.open(file)
    binaryMsg = ''

    # tuples of rgba values Ex:(0,0,0,255)
    rgba = img.getdata()


    for colorDigit in rgba:

        #least significant bit
        lsb = decode(rtoh(colorDigit[0], colorDigit[1], colorDigit[2]))
        if lsb == None:
            pass
        else:
            binaryMsg = binaryMsg + lsb
            #checks if it hits the delimiter
            if (binaryMsg[-8:] == '11111110'):
                print("Message have been decoded.")
                return btos(binaryMsg[:-8])

    return btos(binaryMsg)

#to run it. use terminal python3 codePNG.py -e(or -d) picture.png
def Main():
    parser =argparse.ArgumentParser(description="Encode or Decode Message in PNG")
    parser.add_argument('-e',dest='encode', type=str,help= 'Give PNG file name to encode')
    parser.add_argument('-d',dest='decode', type=str,help= 'Give PNG file name to decode')
    args = parser.parse_args()
    if(args.encode !=None):
        msg =input("Enter a message to hide: ")
        print(hide(args.encode,msg))
    elif (args.decode !=None):
        print(reveal(args.decode))
    else:
        parser.usage

if __name__== '__main__':
    Main()


