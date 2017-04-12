import re
from bs4 import BeautifulSoup


soup = BeautifulSoup(html='<a>test</a>')

# Find all with a specific attribute
tags = soup.find_all(src=True)
tags = soup.select("[src]")

# Find all meta with either name or http-equiv attribute.
soup.select("meta[name],meta[http-equiv]")

# find any tags with any name or source attribute.
soup.select("[name], [src]")

# find first/any script with a src attribute.
tag = soup.find('script', src=True)
tag = soup.select_one("script[src]")

# find all tags with a name attribute beginning with foo
# or any src beginning with /path
soup.select("[name^=foo], [src^=/path]")

# find all tags with a name attribute that contains foo
# or any src containing with whatever
soup.select("[name*=foo], [src*=whatever]")

# find all tags with a name attribute that endwith foo
# or any src that ends with  whatever
soup.select("[name$=foo], [src$=whatever]")

# starting with
soup.find_all("script", src=re.compile("^whatever"))
# contains
soup.find_all("script", src=re.compile("whatever"))
# ends with
soup.find_all("script", src=re.compile("whatever$"))
