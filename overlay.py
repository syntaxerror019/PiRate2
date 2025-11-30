#!/usr/bin/env python3
import tkinter as tk
import sys
import time
import math
import colorsys

def get_ip_from_args():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return "No IP Provided"

class IPOverlay:
    def __init__(self, root, ip_text):
        self.root = root
        self.ip_text = ip_text

        # color animation tuning
        self.speed = 0.12
        self.saturation = 0.35
        self.value = 0.98

        # window: fullscreen topmost overlay
        root.title("IP Overlay")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        try:
            root.attributes("-fullscreen", True)
        except:
            pass

        self.frame = tk.Frame(root)
        self.frame.pack(expand=True, fill="both")

        font_size = max(36, int(root.winfo_screenheight() / 12))
        self.ip_label = tk.Label(self.frame, text=ip_text, font=("Helvetica", font_size, "bold"))
        self.ip_label.pack(expand=True)

        small_size = max(12, int(root.winfo_screenheight() / 50))
        self.sub_label = tk.Label(self.frame, text="Enter the above URL to access PiRate2", font=("Helvetica", small_size))
        self.sub_label.pack(side="bottom", pady=24)

        # close shortcuts
        root.bind("<Escape>", lambda e: root.destroy())
        root.bind("<Button-1>", lambda e: root.destroy())
        root.bind("<Key>", self._on_key)

        # start animation
        self._running = True
        self._animate()

    def _on_key(self, event):
        if event.keysym.lower() in ("q",):
            self.root.destroy()

    def _hsv_to_hex(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
        return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"

    def _contrast_color(self, h, s, v):
        r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
        luminance = 0.2126*r + 0.7152*g + 0.0722*b
        return "#000000" if luminance > 0.5 else "#ffffff"

    def _animate(self):
        if not self._running:
            return

        t = time.time() * self.speed

        # calming blues/purples
        base_hue = 0.65
        range_h = 0.10
        hue = base_hue + math.sin(t) * range_h

        v = self.value * (0.85 + 0.15 * (1 + math.sin(t * 0.7)) / 2)

        bg = self._hsv_to_hex(hue, self.saturation, v)
        fg = self._contrast_color(hue, self.saturation, v)

        self.frame.configure(bg=bg)
        self.ip_label.configure(bg=bg, fg=fg)
        self.sub_label.configure(bg=bg, fg=fg)

        self.root.after(16, self._animate)

def main():
    ip = get_ip_from_args()

    root = tk.Tk()
    IPOverlay(root, ip)
    root.mainloop()

if __name__ == "__main__":
    main()
