daily_sales= [5,10,12,7,3,225,8,9,1,15,16,1,18,1,9]
total_cups = (sale for sale in daily_sales if sale > 5)
print(total_cups)