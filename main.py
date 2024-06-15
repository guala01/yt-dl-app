import tkinter
import customtkinter
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
from pytube import Playlist
import threading

def update_progress_label(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    progressLabel.configure(text=f"Download progress: {percentage:.2f}%")

def startdl():
    try:
        ytlink = link.get()
        # Reset progress label to 0% at the start of a new download
        progressLabel.configure(text="Download progress: 0%")
        
        if "playlist" in ytlink:
            ytobject = Playlist(ytlink)
            title.configure(text="Downloading Playlist", text_color="white")
            finishLabel.configure(text="")
            total_videos = len(ytobject.videos)
            if optionmenu_var.get() == "Audio Only":
                for index, audio in enumerate(ytobject.videos):
                    audio.register_on_progress_callback(update_progress_label)
                    audio.streams.get_audio_only().download()
            elif optionmenu_var.get() == "Highest Quality":
                for index, video in enumerate(ytobject.videos):
                    video.register_on_progress_callback(update_progress_label)
                    video.streams.get_highest_resolution().download()
            elif optionmenu_var.get() == "Low Quality":
                for index, video in enumerate(ytobject.videos):
                    video.register_on_progress_callback(update_progress_label)
                    video.streams.get_lowest_resolution().download()
            else:
                print("var not defined")
                return
            finishLabel.configure(text="Download Completed")
        else:
            ytobject = YouTube(ytlink)
            title.configure(text=ytobject.title, text_color="white")
            finishLabel.configure(text="")
            if optionmenu_var.get() == "Audio Only":
                ytobject.register_on_progress_callback(update_progress_label)
                ytobject.streams.get_audio_only().download()
            elif optionmenu_var.get() == "Highest Quality":
                ytobject.register_on_progress_callback(update_progress_label)
                ytobject.streams.get_highest_resolution().download()
            elif optionmenu_var.get() == "Low Quality":
                ytobject.register_on_progress_callback(update_progress_label)
                ytobject.streams.get_lowest_resolution().download()
            else:
                print("var not defined")
                return
            finishLabel.configure(text="Download Completed")
    except VideoUnavailable:
        finishLabel.configure(text="video unavailable", text_color="red")
    except RegexMatchError:
        finishLabel.configure(text="YouTube link invalid", text_color="red")

def start_download_thread():
    download_thread = threading.Thread(target=startdl)
    download_thread.start()


def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)


def showoptions():
    if app.toplevel_window is None or not app.toplevel_window.winfo_exists():
        optmenu = customtkinter.CTkToplevel(app)
        print(optmenu)
        optmenu.geometry("400x300")
        optmenu.after(10, optmenu.lift)
        label = customtkinter.CTkLabel(optmenu, text="Download Options")
        label.pack()
        optionmenu = customtkinter.CTkOptionMenu(optmenu, values=["Audio Only", "Highest Quality", "Low Quality"],
                                                 command=optionmenu_callback, variable=optionmenu_var)
        optionmenu.pack()
    else:
        app.toplevel_window.focus()


# app appearance
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("yt-dl")
app.toplevel_window = None

# ui elements
title = customtkinter.CTkLabel(app, text="Paste Youtube link")
title.pack(padx=10, pady=10)

# input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack(padx=10, pady=10)

# finish label
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# progress label
progressLabel = customtkinter.CTkLabel(app, text="Download progress: 0%")
progressLabel.pack(padx=10, pady=10)

# download button
download = customtkinter.CTkButton(app, text="Download", command=start_download_thread)
download.pack()

# menu button
optionmenu_var = tkinter.StringVar(value="Highest Quality")
menu = customtkinter.CTkButton(app, text="Download options", command=showoptions)
menu.pack(padx=10, pady=20)

# main loop
app.mainloop()