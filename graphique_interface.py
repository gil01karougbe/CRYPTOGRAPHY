from tkinter import *



def process_input():
    # Get the input text from the entry widget
    input_text = input_area.get() 
    output_text = "Processed: " + input_text
    # Clear previous output
    output_area.delete("1.0", "end")
     # Insert the processed output 
    output_area.insert("1.0", output_text) 


#######------------------TKINTER------------------------#####################
#création de l'instance fenètre
window=Tk()
#personnalisation de la fenètre
window.title("Cryptography") 
window.geometry("1080x720")
window.minsize(480,360)
window.iconbitmap("images\image2.ico")
window.config(background="gray")

# Entry widget for input
input_area = Entry(window, width=50)
input_area.pack(pady=10)

# Button to trigger processing
process_button = Button(window, text="Process", command=process_input)
process_button.pack()

# Text widget for output
output_area = Text(window, width=50, height=10)
output_area.pack(pady=10)



#affichage
window.mainloop()
