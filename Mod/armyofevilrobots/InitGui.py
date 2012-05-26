"""
AOER tool library
"""
import FreeCAD,FreeCADGui

#Workbench is defined in globals apparently...
class AOERBench ( Workbench ):
    "My workbench object"
    Icon = """
            /* XPM */
            static const char *test_icon[]={
            "16 16 2 1",
            "a c #000000",
            ". c None",
            "................",
            "................",
            "..############..",
            "..############..",
            "..############..",
            "..############..",
            "..####....####..",
            "..####....####..",
            "..####....####..",
            "..####....####..",
            "..############..",
            "..############..",
            "..############..",
            "..############..",
            "................",
            "................"};
            """
    #import os
    #Icon = (open(
            #os.path.join(
                #__file__, 'resources', 'menger.xpm'), 'r')
            #.read())
    MenuText = "ArmyOfEvilRobots"
    ToolTip = "Rapid prototyping workbench."

    def GetClassName(self):
        """This is the Class name used in freecad mapping"""
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """Setup"""
        from geometry import menger
        self.appendToolbar("AOER Tools", ["Menger",])
        self.appendMenu("AOER Tools", ["Menger",])
        FreeCADGui.addCommand('Menger', menger.MengerCommand())
        Log ("Loading MyModule... done\n")

    def Activated(self):
        """do something here if needed..."""
        Msg ("AOERBench.Activated()\n")

    def Deactivated(self):
        """do something here if needed..."""
        Msg ("AOERBench.Deactivated()\n")

FreeCADGui.addWorkbench(AOERBench)
