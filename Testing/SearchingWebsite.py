try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = "jav"

for j in search(query, tld="co.in", num=1000000, stop=1000000, pause=2):
    print(j)