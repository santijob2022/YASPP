from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1/10#25
SHORT_BREAK_MIN = 1/12 #5
LONG_BREAK_MIN = 1/6#20

initial_time = 0.2 # in minutes
reps = 0
timer = None # This is used to reset the timer
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    window.after_cancel(timer)
    timer_Label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text=f"00:00")
    check_marks.config(text="")    
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_timer():
    global reps
    reps += 1
    if(reps%8 == 0 ):
        initial_time = LONG_BREAK_MIN
        timer_Label.config(text ="Long Break", fg=RED)
    elif (reps % 2 == 0):
        initial_time = SHORT_BREAK_MIN        
        timer_Label.config(text="Short Break", fg=PINK)
    else:
        initial_time = WORK_MIN    
        timer_Label.config(text="Time to work", fg=GREEN)

    count_down(int(initial_time*60))
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def count_down(counter):
    count_min = math.floor(counter/60)
    if(count_min < 10):
        count_min = '0'+str(count_min)
    count_sec = counter%60
    if(count_sec < 10):
        count_sec ='0'+str(count_sec)
    
    canvas.itemconfig(timer_text,text=f"{count_min}:{count_sec}")
    if counter > 0:
        global timer
        timer = window.after(1000,count_down,counter-1)
    elif counter ==  0:
        window.after(1000, start_timer)
        if (reps%8)%2 ==0:
            check_marks.config(text="✔"*int((reps%8)/2), fg=GREEN)
        

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
##window.minsize(width=220, height=250)
window.config(padx=80,pady=50,bg=YELLOW)

timer_Label = Label(text="Timer",fg=GREEN,font=("Arial",40,"bold"),bg=YELLOW, width=10,height=1)
# width is number of characters, height is number of lines
timer_Label.grid(column=2,row=1)

canvas = Canvas(width=206,height=224,bg=YELLOW,highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(103,112,image=tomato_img)
timer_text = canvas.create_text(103,130,text="00:00",fill="white",font=(FONT_NAME,25,"bold"))
canvas.grid(column=2,row=2)

start_button = Button(text="Start",font=("Arial",12,"bold"),highlightthickness=0,command=start_timer)
start_button.grid(column=1,row=3)

reset_button = Button(text="Reset",font=("Arial",12,"bold"),highlightthickness=0, command=reset_timer)
reset_button.grid(column=3,row=3)

check_marks = Label( bg=YELLOW, font=(FONT_NAME, 15, "bold"))
check_marks.grid(column=2, row=4)

window.mainloop()
