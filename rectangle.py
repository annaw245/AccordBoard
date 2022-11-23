import tkinter as tk     # python 3
# import Tkinter as tk   # python 2

class Example(tk.Frame):
    """Illustrate how to drag items on a Tkinter canvas"""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # create a canvas
        self.canvas = tk.Canvas(width=400, height=400, background="bisque")
        self.canvas.pack(fill="both", expand=True)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple of movable objects
        #self.create_token(50, 100, "white")
        self.init_note("HIIIIIIII")

        addRect = tk.Button(self, text="Add Note", width=20, command=self.create_token)
        addRect.grid(row=2, column=0, padx=10, pady=10)
        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.drag_start)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.drag_stop)
        self.canvas.tag_bind("token", "<B1-Motion>", self.drag)

    def create_token(self, x=200, y=100, color="white"):
        """Create a token at the given coordinate in the given color"""

        self.canvas.create_rectangle(
            x - 25,
            y - 25,
            x + 25,
            y + 25,
            outline=color,
            fill=color,
            tags=("token",),
        )

    def init_note(self, in_text):
        tags = ("token",)
        self.canvas.create_text(50,100, text=in_text, fill="black", tags=tags)
        self.canvas.create_window(50,130, tags=tags)

        x0, y0, x1, y1 = self.canvas.bbox("token")
        margin = 4
        coords = (x0-margin, y0-margin, x1+margin, y1+margin)
        id=self.canvas.create_rectangle(coords, outline="white", fill="white", tags=tags)
        self.canvas.lower(id)

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]

        rect = self.canvas.bbox(self._drag_data["item"])
        self.canvas.addtag_enclosed("drag", *rect)
        print(rect)

        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        self.canvas.dtag("drag", "drag")

    def drag(self, event):
        """Handle dragging of an object"""
        # compute how much the mouse has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        # move the object the appropriate amount
        #self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        self.canvas.move("drag", delta_x, delta_y)

        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()