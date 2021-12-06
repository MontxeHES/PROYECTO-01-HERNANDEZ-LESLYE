import lifestore_file as lf
from functools import reduce
from datetime import datetime as dt

products = lf.lifestore_products
product_catalog = {}

for product in products:
    # print (product)

    product_catalog[product[0]] = {
        "id":product[0],
        "name":product[1],
        "price":product[2],
        "category":product[3],
        "stock":product[4],
        "sales":0,
        "searches":0
    }
 

sales = lf.lifestore_sales

for sale in sales:
    product_catalog[sale[1]]["sales"] = product_catalog[sale[1]]["sales"]+1
        
searches = lf.lifestore_searches

for search in searches:
    product_catalog[search[1]]["searches"] = product_catalog[search[1]]["searches"]+1

sales_by_product = {k:v["sales"] for k,v in product_catalog.items() if v["sales"] != 0}
searches_by_product = {k:v["searches"] for k,v in product_catalog.items() if v["searches"] != 0}

top_sales = sorted(sales_by_product.items(),key=lambda x:x[1],reverse=True)[0:5]
top_sales_products = ",".join("el producto {} con total de ventas {}".format(str(p), str(s)) for p,s in top_sales)
print("el top de los productos mas vendidos es: {}".format(top_sales_products)) 

top_searches = sorted(searches_by_product.items(),key=lambda x:x[1],reverse=True)[0:10]
print(top_searches)

bottom_sales = sorted(sales_by_product.items(),key=lambda x:x[1],reverse=False)[0:5]
print(bottom_sales)

bottom_searches = sorted(searches_by_product.items(),key=lambda x:x[1],reverse=False)[0:10]
print(bottom_searches)

# # print(sales_by_product)
# # print(searches_by_product)
# # print(sales_by_product.items())
# print(ordered_searches[0:10])

category_catalog = {}

for product in product_catalog.values():
    category_catalog.setdefault(product["category"], []).append(product["id"])

# for c,v in category_catalog.items():
#     print(c, len(v))
# validacion de que en algunas categorias no hay suficientes elementos para hacer un top

reviews = lf.lifestore_sales
reviews_by_product = {}

for sale in reviews:
    reviews_by_product.setdefault(sale[1], []).append(sale[2]*1.0)
print(reviews_by_product)

avg_reviews = {k:sum(v)/len(v) for k,v in reviews_by_product.items()}
print(avg_reviews)

top_reviews = sorted(avg_reviews.items(),key=lambda x:x[1],reverse=True)[0:5]
print(top_reviews)

bottom_reviews = sorted(avg_reviews.items(),key=lambda x:x[1],reverse=False)[0:5]
print(bottom_reviews)

total_revenue = reduce(lambda x,y: x+y, [v["price"] * v["sales"] for v in product_catalog.values()])
print(total_revenue)

sales_dates = lf.lifestore_sales
sales_month_year = {}
sales_year = {}

for sale in sales_dates:
    month_year = dt.strptime(sale[3], "%d/%m/%Y").strftime("%m/%Y")
    year = dt.strptime(sale[3], "%d/%m/%Y").strftime("%Y")
    sales_month_year.setdefault(month_year, []).append(product_catalog[sale[1]]["price"])
    sales_year.setdefault(year, []).append(product_catalog[sale[1]]["price"])
        
avg_sales_month = {k:sum(v)/len(v) for k,v in sales_month_year.items()}
sum_sales_year = {k:sum(v) for k,v in sales_year.items()}
sum_month = {k:sum(v) for k,v in sales_month_year.items()}

best_months = []

for year in sales_year.keys():
    months_year = {k:v for k, v in sum_month.items() if year in k}
    best_month_sales = sorted(months_year.items(),key=lambda x:x[1],reverse=True)[0]
    best_months.append(best_month_sales)
print(dict(best_months))




    