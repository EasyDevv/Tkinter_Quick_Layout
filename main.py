import pyperclip
import customtkinter as ctk
import random


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Tkinter Quick Layout")
        self.geometry("800x800")

        max_rows = 5
        max_columns = 5

        self.create_grid(self, max_rows, max_columns)
        self.create_bg_buttons(max_rows, max_columns)

    def create_grid(self, base, max_rows, max_columns, weight=1):
        """
        Creates a grid with the specified number of rows and columns.
        """
        for i in range(max_rows):
            base.grid_rowconfigure(i, weight=weight)
            for j in range(max_columns):
                base.grid_columnconfigure(j, weight=weight)

    def create_bg_buttons(self, max_rows, max_columns):
        """
        Creates a grid of buttons with the specified number of rows and columns.
        Each button is assigned a command that calls the create_frame method with
        the button's row and column indices as arguments.
        """
        for i in range(max_rows):
            for j in range(max_columns):
                button = ctk.CTkButton(
                    self,
                    text="+",
                    fg_color="gray",
                    hover_color="lightgray",
                    command=lambda i=i, j=j: self.create_frame(i, j),
                )
                button.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")

    def create_frame(self, row, column):
        """
        Creates a frame with a random background color and a grid of buttons.
        """
        primary_color, secondary_color, tertiary_color = generate_and_adjust_colors()

        frame = ctk.CTkFrame(self, fg_color=primary_color, corner_radius=0)
        frame.grid(row=row, column=column, sticky="nsew")
        self.add_buttons_to_frame(frame, secondary_color, tertiary_color)

    def add_buttons_to_frame(self, frame, secondary_color, tertiary_color):
        """
        Add buttons to clicked frame.
        """
        self.create_grid(frame, 7, 7, weight=2)
        BUTTON_WIDTH = 35

        info = frame.grid_info()
        row = info["row"]
        column = info["column"]

        # ================================================================
        # Position
        # ================================================================
        label = ctk.CTkLabel(
            frame,
            text=f"row={row}, column={column}\nrowspan=1, columnspan=1",
            text_color="black",
        )
        btn_add_row = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▼",
            fg_color=secondary_color,
            command=lambda: self.change_grid_parameters(frame, label, "row", +1),
        )
        btn_sub_row = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▲",
            fg_color=secondary_color,
            command=lambda: self.change_grid_parameters(frame, label, "row", -1),
        )
        btn_add_column = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▶",
            fg_color=secondary_color,
            command=lambda: self.change_grid_parameters(frame, label, "column", +1),
        )
        btn_sub_column = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="◀",
            fg_color=secondary_color,
            command=lambda: self.change_grid_parameters(frame, label, "column", -1),
        )

        # ================================================================
        # Spans
        # ================================================================
        btn_add_row_span = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▼▼",
            fg_color=tertiary_color,
            command=lambda: self.change_grid_parameters(frame, label, "rowspan", +1),
        )
        btn_sub_row_span = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▲▲",
            fg_color=tertiary_color,
            command=lambda: self.change_grid_parameters(frame, label, "rowspan", -1),
        )
        btn_add_column_span = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="▶▶",
            fg_color=tertiary_color,
            command=lambda: self.change_grid_parameters(frame, label, "columnspan", +1),
        )
        btn_sub_column_span = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="◀◀",
            fg_color=tertiary_color,
            command=lambda: self.change_grid_parameters(frame, label, "columnspan", -1),
        )

        # ================================================================
        # Utilities
        # ================================================================
        btn_copy = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="✓",
            fg_color=secondary_color,
            command=lambda: self.copy_info(frame),
        )
        btn_close = ctk.CTkButton(
            frame,
            width=BUTTON_WIDTH,
            text="X",
            fg_color=secondary_color,
            command=lambda: self.close_frame(frame),
        )

        # ================================================================
        # Grid
        # ================================================================
        label.grid(row=0, column=1, columnspan=5, padx=20, pady=5, sticky="nsew")
        btn_sub_row.grid(row=2, column=3, padx=0, pady=0)
        btn_add_row.grid(row=4, column=3, padx=0, pady=0)
        btn_add_column.grid(row=3, column=4, padx=0, pady=0)
        btn_sub_column.grid(row=3, column=2, padx=0, pady=0)

        btn_sub_row_span.grid(row=1, column=3, padx=0, pady=0)
        btn_add_row_span.grid(row=5, column=3, padx=0, pady=0)
        btn_add_column_span.grid(row=3, column=5, padx=0, pady=0)
        btn_sub_column_span.grid(row=3, column=1, padx=0, pady=0)
        btn_copy.grid(row=3, column=3, padx=0, pady=0)
        btn_close.grid(row=5, column=5, padx=0, pady=0)

    def change_grid_parameters(self, frame, label, param="row", operation=+1):
        """
        Changes the specified grid parameter of the frame.
        """
        if param not in {"row", "column", "rowspan", "columnspan"}:
            raise ValueError(f"Invalid parameter: {param}")

        min_value = 1 if "span" in param else 0

        var = frame.grid_info()[param] + operation
        var = max(var, min_value)

        if param == "row":
            frame.grid(row=var)
        elif param == "column":
            frame.grid(column=var)
        elif param == "rowspan":
            frame.grid(rowspan=var)
        elif param == "columnspan":
            frame.grid(columnspan=var)

        info = frame.grid_info()
        row = info["row"]
        column = info["column"]
        row_span = info["rowspan"]
        column_span = info["columnspan"]

        label.configure(
            text=f"row={row}, column={column}\n rowspan={row_span}, columnspan={column_span}"
        )

    def copy_info(self, frame):
        """
        Copies the frame's grid information to the clipboard.
        """
        info = frame.grid_info()

        pyperclip.copy(
            f"row={info['row']}, column={info['column']}, rowspan={info['rowspan']}, columnspan={info['columnspan']},"
        )

    def close_frame(self, frame):
        frame.destroy()


def generate_and_adjust_colors(factor1=0.6, factor2=0.4):
    """
    Generates a random color and returns it along with two adjusted versions.
    """
    r, g, b = (random.randint(0, 255) for _ in range(3))
    primary_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

    second_r, second_g, second_b = (max(0, int(color * factor1)) for color in (r, g, b))
    secondary_color = "#{:02x}{:02x}{:02x}".format(second_r, second_g, second_b)

    third_r, third_g, third_b = (max(0, int(color * factor2)) for color in (r, g, b))
    tertiary_color = "#{:02x}{:02x}{:02x}".format(third_r, third_g, third_b)

    return primary_color, secondary_color, tertiary_color


def adjust_rgb(r, g, b, factor=0.8):
    """
    Adjusts the specified RGB color by the specified factor.
    """
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))
    return r, g, b


if __name__ == "__main__":
    try:
        print("Starting...")
        app = App()
        app.mainloop()
    except Exception as e:
        with open("error.txt", "w") as f:
            f.write(e)
