"""
Application class that implements pyFoamChangeBoundaryName.py

Author:
  Martin Beaudoin, Hydro-Quebec, 2010.

"""

from PyFoamApplication import PyFoamApplication

from os import path
import sys
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.RunDictionary.ListFile import ListFile

class ChangeBoundaryName(PyFoamApplication):
    def __init__(self,args=None):
        description="""
Changes the name of a boundary in the boundary-file
        """
        PyFoamApplication.__init__(self,args=args,
                                   description=description,
                                   usage="%prog <caseDirectory> <boundaryName> <new name>",
                                   changeVersion=False,
                                   nr=3,
                                   interspersed=True)
        
    def addOptions(self):
        self.parser.add_option("--test",
                               action="store_true",
                               default=False,
                               dest="test",
                               help="Only print the new boundary file")

    def run(self):
        fName=self.parser.getArgs()[0]
        bName=self.parser.getArgs()[1]
        nName=self.parser.getArgs()[2]

        boundary=ParsedParameterFile(path.join(".",fName,"constant","polyMesh","boundary"),debug=False,boundaryDict=True)

        bnd=boundary.content

        if type(bnd)!=list:
            print "Problem with boundary file (not a list)"
            sys.exit(-1)

        found=False

        for val in bnd:
            if val==bName:
                found=True
            elif found:
                bnd[bnd.index(bName)]=nName
                break

        if not found:
            print "Boundary",bName,"not found in",bnd[::2]
            sys.exit(-1)

        if self.opts.test:
            print boundary
        else:
            boundary.writeFile()
            self.addToCaseLog(fName)
