names = ["Samyak","Pranika","Joe","Piyush","Hitesh"]
price = ["100","200","300","40","50"]

combined_data = zip(names,price)



for name , price in combined_data : 
    print (f"Name : {name} Paid : {price}")