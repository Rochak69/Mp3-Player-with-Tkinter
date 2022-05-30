from tkinter import *
from tkinter import filedialog
from tracemalloc import stop
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
root= Tk()
root.title('Mp3 Player')
root.geometry("500x352")

#initilaize pygame
pygame.mixer.init()
#Function for time
def play_time():
    if is_stop:
        return
    current_time= pygame.mixer.music.get_pos()/1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

	# Reconstruct song with directory structure stuff
    song = playlist_box.get(ACTIVE)
    song = f'C:/Users/Rochak/Desktop/Mp3player/audio/{song}'
    song_mut= MP3(song)
    global song_length
    song_length= song_mut.info.length
    converted_song_length= time.strftime('%M:%S', time.gmtime(song_length))
    
    if int(song_slider.get())== int(song_length):
        stop()

    elif paused:
        pass
    else:
    #Move slider along song
        next_time= int(song_slider.get()) +1 

        song_slider.config(to=song_length, value=next_time)
    #Conver slider position to time format
    converted_current_time = time.strftime('%M:%S', time.gmtime(int(song_slider.get())))
    #Output stauts bar
    status_bar.config(text=f'Timpe elapsed= {converted_current_time} of {converted_song_length}    ')

    if current_time >=1:
        status_bar.config(text=f'Timpe elapsed= {converted_current_time} of {converted_song_length}    ')
    status_bar.after(1000, play_time)
    
    


def slide(x):
    song=playlist_box.get(ACTIVE)
    #Reconstruct directory
    song=f'C:/Users/Rochak/Desktop/Mp3player/audio/{song}'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=song_slider.get())
    

def add_mp3_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3" ), ))
    for song in songs:
        song = song.replace("C:/Users/Rochak/Desktop/Mp3player/audio/", "")
        #song = song.replace(".mp3", "")
	    # Add To End of Playlist
        playlist_box.insert(END, song)

def add_wav_songs():
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("WAV Files", "*.wav" ), ))
    for song in songs:
        song = song.replace("C:/Users/Rochak/Desktop/Mp3player/audio/", "")
	    # Add To End of Playlist
        playlist_box.insert(END, song)

#delete
def delete_song():
    playlist_box.delete(ANCHOR)

def delete_all_songs():
    playlist_box.delete(0,END)

#Play function
def play():
    #set stop to false
    global is_stop
    is_stop= False
   
    song=playlist_box.get(ACTIVE)
    #Reconstruct directory
    song=f'C:/Users/Rochak/Desktop/Mp3player/audio/{song}'
    
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()

global is_Stop
is_stop=False
#Stop a song
def stop():
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)
    status_bar.config(text='')

    #manage slider
    song_slider.config(value=0)
    global is_stop
    is_stop= True

#Create pause variable
global paused
paused= False
#Pause song
def pause(is_paused):
    global paused
    paused= is_paused
    if paused:
        pygame.mixer.music.unpause()
        paused= False
    else:
         pygame.mixer.music.pause()
         paused= True

#Forward a song
def next_song():
    #Reset slider postition and status bar
    status_bar.config(text="")
    song_slider.config(value=0)
    next_one= playlist_box.curselection()
    next_one= next_one[0] +1
    song= playlist_box.get(next_one)
    song=f'C:/Users/Rochak/Desktop/Mp3player/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist_box.selection_clear(0,END)
    playlist_box.activate(next_one)
    playlist_box.selection_set(next_one, last=None)

#Previous song
def previous_song():
    status_bar.config(text="")
    song_slider.config(value=0)
    next_one= playlist_box.curselection()
    next_one= next_one[0] -1
    song= playlist_box.get(next_one)
    song=f'C:/Users/Rochak/Desktop/Mp3player/audio/{song}'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlist_box.selection_clear(0,END)
    playlist_box.activate(next_one)
    playlist_box.selection_set(next_one, last=None)
#create mainframe
main_frame= Frame(root)
main_frame.pack(pady=20)
    
#Create Playlist Box
playlist_box= Listbox(main_frame, font=("Arial",10), bg="white", fg="black", selectbackground="#2596be", selectforeground="White", width=60, height=10)
playlist_box.grid(row=0, column=0)

#Create song slider
song_slider = ttk.Scale(main_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=slide)
song_slider.grid(row=1, column=0, pady=(15,3))
 

#Images for button
back_btn_img= PhotoImage(file='images/back50.png')
forward_btn_img= PhotoImage(file='images/forward50.png')
play_btn_img= PhotoImage(file='images/play50.png')
pause_btn_img= PhotoImage(file='images/pause50.png')
stop_btn_img= PhotoImage(file='images/stop50.png')

#Create button frame
control_frame= Frame(main_frame)
control_frame.grid(row=3, column=0, pady=12)
#create button
back_button= Button(control_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button= Button(control_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button= Button(control_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button= Button(control_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button= Button(control_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)

#Create Menu
my_menu= Menu(root)
root.config(menu=my_menu)

#Create Add Song Menu Dropdonwm
add_song_menu= Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Add songs", menu=add_song_menu)


add_song_menu.add_command(label="Add MP3 songs", command=add_mp3_songs)
add_song_menu.add_command(label="Add WAV songs", command=add_wav_songs)

#Create delete
remove_song_menu= Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Remove songs", menu= remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from playlist", command=delete_all_songs)

#status bar
status_bar= Label(main_frame, text="", fg="#2596be", font=("Arial",11),  anchor=E)
status_bar.grid(row=2, column=0, pady=0)

pygame.mixer.init()

root.mainloop()
