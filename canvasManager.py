# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 17:24:27 2021

@author: Main Floor
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:58:57 2021

@author: Main Floor
"""

from tkinter import *
from ToolTip.ToolTip import ToolTip
from Edit_Display.CanvasTextEdit import CanvasTextEdit
from Highlight.Highlight import MouseoverHighlight
from PopupMenu.PopupMenu import PopupMenu
from intraCanvasManager.CanvasInsertDelete import CanvasInsertDelete

debugging = True

class canvasManager:


    Event               = None
    valid_justification = ["nw", "ne"]
    Canvas_Items        = ["arc", "bitmap", "image", "line", "oval", "polygon",
                    "rectangle", "text", "window"]

    def __init__(self, listofCanvas, canvas, root, justification = "nw" ):

        self.Buffer = [0, 10]
        self.BufferFirst = [10, 10]

        self.config_check(listofCanvas, canvas, root, justification)          # Confirms that the inputs are valid
        self.PopupMenu()                                                       # Initializes the popup menu

        self.emptyCanvas()



    def config_check(self, listofCanvas, canvas, root, justification):
        """" configuration of CanvasInsertDelete """

        if root != None:                                              # Only Test if the listofwidgets has been updated
            if ( (root.__class__.__name__ != Tk.__name__) &                    # Test to find out if the Root is a Window or Frame
                ( root.__class__.__name__ != Frame.__name__) ):
                raise TypeError ("<Root> must be a Window or a Frame")
            else:
                self.Root = root                                               # Valid Root Object

        if canvas != None:
            if (canvas.__class__.__name__ != Canvas.__name__) :                   # Test to find out if the Canvas is a tkinter Canvas Widget
                raise TypeError ("<canvas> must be a Canvas Widget")
            else:
                self.Canvas = canvas

        if listofCanvas != None:
            if len(listofCanvas) > 0:
                for element in listofCanvas:
                    handler = element[0]                                       # [Widget, embued properties, position, buffer space]
                    if handler != Canvas.__name__:
                        raise TypeError("<listofCanvas> variable must contain valid Canvas type Widgets")
                    else:
                        self.listofCanvas = listofCanvas

            else:
                self.listofCanvas = []



        if justification != None:
            if type(justification) == str:
                if justification not in canvasManager.valid_justification:
                    raise TypeError ("<justification> is invalid, please check your justification settings")
                else:
                    self.justification = justification



    def config(self, listofCanvas = None, canvas = None, root = None, justification = None):
        self.config_check(listofCanvas, canvas, root, justification)          # Send the variables to the configuration update
        self.update()                                                          # update any justification if need be


    def emptyCanvas(self):

        if self.listofCanvas == []:


            # self.listofwidgets = [ [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer],
            #                        [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer] ]
            Xnext = self.BufferFirst[0]
            Ynext = self.BufferFirst[1]
            subCanvas = Canvas(self.Root)
            subCanvas_Window = self.Canvas.create_window(Xnext, Ynext, window = subCanvas)
            embuedproperties = self.createNew(subCanvas, subCanvas_Window)
            Position = [Xnext, Ynext]
            Buffer = self.BufferFirst
            self.listofCanvas.insert(0, [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer])
            self.update()

            if debugging == True: print("Empty Canvas, New subCanvas Made")






    def insert(self, event):
        ''' Activated when a new widget is inserted into the canvas. Ensures
        the widget is added to the list. Preforms all instantiation operations
        for a adding a widget to a list'''

        # self.listofCanvas = [ [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer],
        #                       [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer] ]


        print("Clicked Widget Position: ", event.x, event.y)

        #find the position of the widget in the list
        index, subCanvas_Window = self.whichCanvas(event)
        if (index, subCanvas_Window) != (-1, 0):                                  # Catch for if widget doesn't exist anymore
                                                                               # Why does this actually become a problem?

            position = self.Canvas.bbox(subCanvas_Window)                         # Actual Position of Anchor Position
            print("Position", position)
            print("Coordinates", self.Canvas.coords(subCanvas_Window))
            print("Buffer", self.Buffer)
            xmin = position[0]
            xmax = position[2]
            ymin = position[1]
            ymax = position[3]
            if self.justification == "nw":                                          # Anchor Position in NW corner
                ymax = ymin + (ymax-ymin) + self.Buffer[1]                          # bbox seems to be out by a pixel or two
                Xnext = xmin                                                      # ymax may be a slight number of pixels incorrect
                if debugging == True: print("Xmin", xmin, "Xnext", Xnext)
                Ynext = ymax + self.Buffer[1]                                       # but still close enough




            if self.justification == "ne":
                ymax = ymin + (ymax - ymin)                                  # bbox seems to be out by a pixel or two
                Xnext = xmin
                Ynext = ymax + self.Buffer[1]



            subCanvas = Canvas(self.Root)
            print("Xnext: ", Xnext, "Ynext: ", Ynext)
            subCanvas_Window = self.Canvas.create_window(Xnext, Ynext, window = subCanvas, anchor = self.justification)


            embuedproperties = self.createNew(subCanvas, subCanvas_Window)

            Position = [Xnext, Ynext]
            Buffer = self.Buffer
            self.listofCanvas.insert(index + 1, [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer ])
            self.update()

            if debugging == True: print("insert complete" )
            #self.Canvas.coords(subCanvas_Window, [Xnext, Ynext])
            if debugging == True: print("subcanvas position: ", self.Canvas.bbox(subCanvas_Window))





        pass

    def whichCanvas(self, event):
        ''' Using the Relative XY coordinates of where a Mouse button press
        occured in the canvas, the function determines which widget was pressed.
        However, I am unsure of what happens when or if the canvas has a
        scrollbar. This may require some more future modifications. '''

        #currentWidget = event.widget


        #find the position of the widget in the list
        index = 0
        #Find Position of previous Widget

        for element in self.listofCanvas:
            subCanvas_Window = element[1]

            position = self.Canvas.bbox(subCanvas_Window)                                #bbox surrounds the widget by 1 pixel

            #print("Widget position: ", self.Canvas.bbox(widget))
            #print("Widget Position: ", self.Canvas.coords(widget))

            xmin = position[0]
            xmax = position[2]

            ymin = position[1]
            ymax = position[3]

            if (xmin <= event.x) & (event.x <= xmax):
                if (ymin <= event.y) & (event.y <= ymax):
                    current_subCanvas_Window = subCanvas_Window
                    return index, current_subCanvas_Window
                    break

            index = index + 1
            if debugging == True: print("Which item was clicked? ", index)

        return -1, 0                                                           #no matching widget found

    def remove(self, event):

        if debugging == True: print("Remove activated")

        # self.listofCanvas = [ [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer],
        #                       [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer] ]
        #                       [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer] ]

        index, subCanvas_Window = self.whichCanvas(event)
        subCanvas = self.listofCanvas[index][0]

        if (index, subCanvas_Window) != (-1, 0):                                  # Only Remove a Widget that Exists (catch for double remove)
            print(len(self.listofCanvas))
            if len(self.listofCanvas) > 1:
                #self.listofCanvas[index][2][1].tkinter_widget_leave() #induce tooltip leave upon deletion of widget
                self.Canvas.delete(subCanvas_Window)
                subCanvas.destroy()

                if debugging == True: print("Which Widget")
                self.listofCanvas.pop(index)
                self.update()

            else:
                #self.listofCanvas[index][2][1].tkinter_widget_leave()   #induce tooltip leave upon deletion of widget
                self.Root.bell()
                messagebox.showwarning("Last Entry", "Don't delete the last text entry")
                self.Canvas.delete(subCanvas_Window)
                subCanvas.destroy()

                if debugging == True: print("Which Widget")
                self.listofCanvas.pop(index)
                self.update()
                self.emptyCanvas()

    def update(self):
        ''' When a widget is added or deleted, the canvas needs to be updated.
        The position of each widget is updated after a widget is added or
        removed '''
        # self.listofwidgets = [ [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer],
        #                        [subCanvas, subCanvas_Window, embuedproperties, Position, Buffer] ]

        index = 0
        for currentWidgetEntry in self.listofCanvas:
            if debugging == True: print("***********************************")
            if debugging == True: print("Current Widget: ", index)
            currentWidget = currentWidgetEntry[1]                             # handler to the current widget
            self.Canvas.itemconfig(currentWidget, anchor = self.justification)

            if debugging == True: print("Current Position: ", currentWidgetEntry[2])

            if index == 0:                                                     # First Widget Special Case
                X = currentWidgetEntry[3][0]                                   # Return X Buffer Distance
                Y = currentWidgetEntry[3][1]                                   # Return Y Buffer Distance
                #print("Buffer Space: ", X, Y)
                if self.justification == 'ne':                                 # Modify XY if Right Justified ("ne")
                    canvas_width = self.Canvas.winfo_width()                   # Width of Canvas
                    X = canvas_width - self.BufferFirst[0]                     # NE anchor = Width of Canvas - Buffer Distance
                    Y = self.BufferFirst[1]
                else:
                    X = self.BufferFirst[0]
                    Y = self.BufferFirst[1]
                self.Canvas.coords(currentWidget, X, Y)                        # Move the Widget to this position
                self.listofCanvas[index][4] = [X, Y]                          # Rerecord this position (why?)
                if debugging == True: print("New Position: ", currentWidgetEntry[3])

            else:                                                              # Every Other Widget Normal Case
                previousWidgetEntry = self.listofCanvas[index - 1]             # Previous Widget Column Vector
                previousWidget = previousWidgetEntry[1]                        # Window Handler
                previous_X = self.Canvas.coords(previousWidget)[0]             # Previous Widget Anchor X Position
                previous_Y = self.Canvas.coords(previousWidget)[1]             # Previous Widget Anchor Y Position
                coordinates = self.Canvas.bbox(previousWidget)               # Previous Widget Bounding Box [xmin, ymin, xmax, ymax]
                                                                               # xmin, ymin is top left corner
                                                                               # xmax, ymax is bottom right corner
                height = coordinates[3] - coordinates[1]
                width = coordinates[2] - coordinates[0]

                if debugging == True: print("Width: ", width, "Heigh: ", height)


                previousWidget_refX = previous_X
                previousWidget_refY = previous_Y + height


                Buffer = currentWidgetEntry[4]
                Buffer_X = Buffer[0]
                Buffer_Y = Buffer[1]

                if debugging == True: print("Buff_X: ", Buffer_X, "Buff_Y: ", Buffer_Y)

                new_X = previousWidget_refX + Buffer_X
                new_Y = previousWidget_refY + Buffer_Y

                position = [new_X, new_Y]

                if debugging == True: print("New X: ", new_X, "New Y: ", new_Y)

                self.Canvas.coords(currentWidget, new_X, new_Y)

                self.listofCanvas[index][2] = position

            if debugging == True: print("Update Complete")

            index = index + 1





        pass

    def createNew(self, subCanvas, subCanvas_Window):
        ''' Create a new widget, endow the widget with all of the desired
        properties using this method. '''
        listofproperties = []


        feature = CanvasInsertDelete([], subCanvas, self.Root)                 # Each Canvas Object is a CanvasInsertDelete Object
        listofproperties.append(feature)
        #feature = ToolTip(subCanvas, text = "Right Click bring up popup menu") # Tooltip Popup upon mouseover
        #listofproperties.append(feature)
        #needs to be modified to work with canvases ***********************************************
        feature = MouseoverHighlight(subCanvas, self.Root, self.Canvas, 0x02, OutlineWidth=5, window = True)     # Highlight upon Mouseover
        listofproperties.append(feature)
        feature = PopupMenu(subCanvas, self.Root, self.Canvas, self.Menu, self, window = True)   # Popup Menu Upon Right Click
        listofproperties.append(feature)
        feature = self.PopupMenu_feature(subCanvas)                               # Auto-Update Popup Menu Functions
        listofproperties.append(feature)


        return listofproperties

    def PopupMenu(self, event = None):

        self.Menu = Menu(Root, tearoff = 0)
        self.Menu.add_command(label = "Insert Below  " )
        self.Menu.add_command(label = "Remove Current")
        self.SubMenu = Menu(self.Menu)
        self.SubMenu.add_command(label = "LHS Justification", command = (lambda: self.configUpdate(justification = 'nw')))
        self.SubMenu.add_command(label = "RHS Justification", command = (lambda: self.configUpdate(justification = 'ne')))
        self.Menu.add_cascade(label = "Justification", menu = self.SubMenu)

    def PopupMenu_feature(self, Widget):
        Widget.bind("<Button-3>", self.PopupMenu_update, add = '+')

    def PopupMenu_update(self, event = None  ):

        if event != None:
            CanvasInsertDelete.Event = event
            if debugging == True: print("Event:" , CanvasInsertDelete.Event.x)

        Event = CanvasInsertDelete.Event

        self.Menu.entryconfig("Insert Below  ", command = (lambda: self.insert(Event) ) )
        self.Menu.entryconfig("Remove Current", command = (lambda: self.remove(Event) ) )


    def returnWidgets(self):
        pass





if __name__ == "__main__":



    debugging = True
    Root = Tk()

    Root.focus_set()

    Button_ = Button(Root, text = "Test")
    Button_.pack()

    canvas = Canvas(Root, width = 400, height = 800)
    canvas.config(bg = "gray")
    canvas.pack()

    canvas.create_text(0,0, text = "Test", anchor = NW)
    canvas.create_text(0,380, text = "Test", anchor = NW)
    listofwidgets = []

    # self.listofwidgets = [ [Widget, embued properties, Position, Buffer Space],
    #                        [Widget, embued properties, Position, Buffer Space] ]

    #canvasText = canvas.create_text(10, 10, text = "Default Text", anchor = NW)

    #canvasTextEdit    = CanvasTextEdit(canvasText, canvas, Root)
    #canvasTextToolTip = ToolTip(canvasText, Root, canvas, text = "Right click to insert below")
    #if debugging == True: print(canvas.coords(canvasText))
    #canvas.coords(canvasText, 10, 10)
    #if debugging == True: print(canvas.coords(canvasText))
    #listofwidgets.append([canvasText, [canvasTextEdit, canvasTextToolTip], [10, 10], [10, 10]])




    CanvasWidgetManager = canvasManager(listofwidgets, canvas, Root)
    Button2 = Button(Root, text = "Test again")
    window = canvas.create_window(0, 400, window = Button2, anchor = NW)

    ToolTip(Button2)

    MouseoverHighlight(Button2, Root, canvas, 0x02, OutlineWidth=5, window = True)     # Highlight upon Mouseover






    def callback(event, number = 5):
        print("Event: ", event)
        print("Number: ", number)
        Button_.unbind(bind_reference)
        print(Button_.winfo_pointerxy())

        print(Root.winfo_rootx() )
        #print(canvasText.winfo_rootx())
        print("Window size: ", canvasText.winfo_screenheight())



    #canvas.tag_bind(canvasText, '<Button-3>', CanvasWidgetManager.insert, add = '+')

    #bind_reference = Button_.bind("<Enter>", lambda event: callback(event, 5))

    Root.mainloop()


