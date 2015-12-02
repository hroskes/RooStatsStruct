import MakePDF

flavors = (
           "2e2mu",
#           "4e",
#           "4mu",
          )

class MakePDF_Heshy(MakePDF.MakePDF):
    def __init__(self):
        for flavor in flavors:
            self.makeWorkspace(flavor)

    def makeWorkspace(self, channelCode):
        on_off_Code = 0
        MakePDF.MakePDF.makeWorkspace(self, channelCode, on_off_Code)

if __name__ == '__main__':
    MakePDF.turnoffbkg = True
    MakePDF_Heshy()
    MakePDF.ROOT.reset()
    MakePDF.turnoffbkg = False
    MakePDF_Heshy()
