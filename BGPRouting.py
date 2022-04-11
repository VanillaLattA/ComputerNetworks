NonRoutedIPs = []
with open("IPList.txt") as IPFile: #open the file and split lines
    NonRoutedIPs = IPFile.read().splitlines()

#create DataBase and then get output
PrefixToIPPlusASN = {}
with open("DB_091803.txt") as Database:
    IPPlusPrefixLengthPlusASNs = Database.read().splitlines()
    for IPPlusPrefixLengthPlusASN in IPPlusPrefixLengthPlusASNs:
        IPPlusPrefixLengthPlusASNIndividuals = IPPlusPrefixLengthPlusASN.split()

        if (len(IPPlusPrefixLengthPlusASNIndividuals) > 0):
            IP = IPPlusPrefixLengthPlusASNIndividuals[0]
            PrefixLength = int(IPPlusPrefixLengthPlusASNIndividuals[1])
            ASN = IPPlusPrefixLengthPlusASNIndividuals[2]

            IPNumbers = IP.split(".")
            IPBinaryString = ""
            ValidIP = True

            for IPNumber in IPNumbers:
                if (len(IPNumber.strip()) == 0):
                    ValidIP = False
                    break
                
                IPNumberBinaryString = bin(int(IPNumber))[2:]
                while (len(IPNumberBinaryString) < 8):
                    IPNumberBinaryString = "0" + IPNumberBinaryString

                IPBinaryString += IPNumberBinaryString

            if (ValidIP):
                IPPrefixString = IPBinaryString[0:PrefixLength]
                PrefixToIPPlusASN[IPPrefixString] = [IP, ASN, PrefixLength]

#Create dictionary, split the string, search string and print output
NonRoutedIPToIPAndASN = {}
NonRoutedIPToMaxPrefix = {}
for NonRoutedIP in NonRoutedIPs:
    IPNumbers = NonRoutedIP.split(".")
    NonRoutedIPBinaryString = ""
    ValidIP = True

    for IPNumber in IPNumbers:
        IPNumberBinaryString = bin(int(IPNumber))[2:]
        while (len(IPNumberBinaryString) < 8):
            IPNumberBinaryString = "0" + IPNumberBinaryString

        NonRoutedIPBinaryString += IPNumberBinaryString

    for Prefix, IPPlusASN in PrefixToIPPlusASN.items():
        if (NonRoutedIPBinaryString[0:IPPlusASN[2]] == Prefix):
            if (NonRoutedIP not in NonRoutedIPToMaxPrefix or
                IPPlusASN[2] > NonRoutedIPToMaxPrefix[NonRoutedIP]):
                NonRoutedIPToIPAndASN[NonRoutedIP] = [IPPlusASN[0], IPPlusASN[1], IPPlusASN[2]]
                NonRoutedIPToMaxPrefix[NonRoutedIP] = IPPlusASN[2]

#print output: DestinationIP and value of stuff
for NonRoutedIP, DestinationIPAndASNAndPrefixLength in NonRoutedIPToIPAndASN.items():
    print(DestinationIPAndASNAndPrefixLength[0] + "/" + str(DestinationIPAndASNAndPrefixLength[2]) + " "
          + str(DestinationIPAndASNAndPrefixLength[1]) + " " + str(NonRoutedIP))

    
