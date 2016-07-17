import urllib2
from bs4 import BeautifulSoup
import re

class Recipe:
	def __init__(self, title, ingredients, texts):
  		self.title = title
		self.ingredients = ingredients
		self.texts = texts

def get_html(link):
	return urllib2.urlopen(link).read()

def get_recipe_links(overview_page_soup):
	return overview_page_soup.select("div.pf-content li > a")
	

def get_title(recipe_soup):
	return recipe_soup.find("h1").string

def get_ingredients(recipe_soup):
	for strong_text in recipe_soup.select("div.pf-content p > strong"): #the 'Zutaten' headline is in a strong-tag
		if (strong_text.string):
			if ("Zutaten" in strong_text.string):
				for sibling in strong_text.parent.find_next_siblings(limit = 3): #within the next 3 siblings definitely is the ingredient's p-tag where the 'list' is
					if (len(sibling.find_all("br")) > 3): #the ingredients aren't a list, they are br-tag separated texts -> there have to be many br-tags
						return list(sibling.stripped_strings) #strip away all those br-tags, return as list
			else:
				print("Skipped 'NoneType' while searching for beginning of ingredients!")
	print("Couldn't find any ingredients!")
	return ["Keine Zutaten"]
					
def get_text(recipe_soup):
	for strong_text in recipe_soup.select("div.pf-content p > strong"): #the 'Zubereitung' headline is in a strong-tag
		if (strong_text.string):
	                if ("Zubereitung" in strong_text.string):
				texts = []
                	        for sibling in strong_text.parent.find_next_siblings("p"):
					for strong_text_2 in sibling.find_all("strong"):
						if (strong_text_2.string):
							if ("Kosten" in strong_text_2.string or "Preis" in strong_text_2.string or "Geld" in strong_text_2.string):
								return texts
						else:
							print("Skipped 'NoneType' while searching for end of instructions!")
					texts += sibling.stripped_strings
				print("There's probably the cost comparasion in the instructions and couldn't filtered out!")
				return texts
		else:
			print("Skipped 'NoneType' while searching for beginning of instructions!")
	print("Couldn't find any making instructions!")
	return ["Keine Anweisungen"]
					

def get_recipe(link):
	s = BeautifulSoup(get_html(link), "lxml")
	title = get_title(s)
	print("==================================================")
	print("Processing '%s'" % title)
	return Recipe(title, get_ingredients(s), get_text(s))
	

root_soup = BeautifulSoup(get_html("http://feinkostpunks.de/fix-ohne-fix/"), "lxml")

for link_a in get_recipe_links(root_soup):
	recipe = get_recipe(link_a["href"])
