from Tkinter import *
from fractions import gcd
import numpy as np

def save():
    global output, e, root
    contents = output.get(1., 'end-1c')
    name= e.get() #takes the value from the entry
    f=open('/Users/Mohammed/Desktop/'+name, 'w')
    f.write(contents)
    f.close()
    root.destroy()

def generatePrime(length):
    import math
    from Crypto.Util import number
    primeNum = number.getPrime(int(math.log((10**length),2)))
    return int(primeNum)

def choose_e(phi):
    e=0
    while gcd(phi,e)!= 1:
        e=np.random.randint(3,phi)
    return e

def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi

    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2

        x = x2- temp1* x1
        y = d - temp1 * y1

        x2 = x1
        x1 = x
        d = y1
        y1 = y

    if temp_phi == 1:
        return d + phi

def generate_keypair(p, q):
    from fractions import gcd

    n = p * q
    phi = (p-1) * (q-1)
    e = choose_e(phi)
    d = multiplicative_inverse(e, phi)

    return ((e, n), (d, n))


#t1=input("What is the length of the first prime in base 10? ")
#t2=input("What is the length of the second prime in base 10? ")

t1=3
t2=3

p=generatePrime(t1)
q=generatePrime(t2)


while p==q:
    q=generatePrime(t2)
public , private =generate_keypair(p, q)


n=public[1]

e=public[0]
d=private[0]

def encrypt(pk, plaintext):
    key, n = pk
    cipher = [int((ord(char) ** key) % n) for char in plaintext]
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr((char ** key) % n) for char in ciphertext]
    return ''.join(plain)

def copy():
    global textbox,root, output
    contents =textbox.get(1.,'end-1c')
    output.delete(1., END)
    output.insert(1.,contents)

def encry():
    global textbox,root, output, public
    contents =textbox.get(0.,'end-1c')
    encrypted=encrypt(public,contents)
    output.delete(0., END)
    output.insert(0.,encrypted)

def decry():
    global textbox,root, output, private
    contents =textbox.get(0.,'end-1c')
    decrypted=decrypt(private,eval(contents))
    output.delete(0., END)
    output.insert(0.,decrypted)


root = Tk()
root.title("RSA Encryptor")

#Frame
f1=Frame(root)
f1.pack()


#Frame
Label(f1,text="Welcome to the encrypter").pack()
Label(f1,text="Please enter your message").pack()


g2=Label(f1,text="Public Key = " + str(public)).pack()


textbox = Text(root, bg='#2F4F4F', fg='white', height =10)
textbox.pack(pady=10, padx=10)

g=Frame(root)
g.pack()


Label(g, text='Decrypted/Encrypted message below').grid(row=2)

output=Text(root,height =10, bg='#2F4F4F', fg='white')
output.pack(pady=10, padx=10)

#lower frame construction
f=Frame(root)
f.pack()

# more labels and shit
l=Label(f, text='File name:')
l.grid(column=2, row= 3)

Label(f, text='').grid(row =2)

e=Entry(f)
e.grid(column= 3 , row= 3)


#Buttons
Button(f, command=save, text='Save', activeforeground='red').grid(column= 5 , row = 3  )
Button(f, command= encry, text= 'Encrypt ' , activeforeground='red').grid( column = 1 , row = 1 )
Button(f, command= decry, text= 'Decrypt ' , activeforeground='red').grid( column = 3 , row = 1 )
Button(f, command = root.destroy, text= "Quit", bg= "blue" ).grid(column = 0, row = 3)


#Grid/pack/place? can be used to position them pack is one after the others

Label(f,text='',width = 5).grid(column =1 , row =  3 )
Label(f,text='',width = 5).grid(column =4 , row =  3 )


root.mainloop()
