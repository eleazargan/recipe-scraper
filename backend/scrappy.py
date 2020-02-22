from googlesearch import search
from bs4 import BeautifulSoup
import requests
import sys

def scrapgoogle(search_term):
    ingredients = []
    directions = []
    URL = 'https://www.allrecipes.com/search/results/?wt=' + search_term
    page = requests.get(URL)

    soup = BeautifulSoup("%s" %(page.content), "html.parser")
    tags = soup.findAll("article", {"class": "fixed-recipe-card"})

    infosoup = BeautifulSoup("%s" %(tags[0]), "html.parser")
    infodiv = infosoup.findAll("div", {"class": "fixed-recipe-card__info"})

    asoup = BeautifulSoup("%s" %(infodiv[0]), "html.parser")
    links = asoup.findAll("a", {"class": "fixed-recipe-card__title-link"})
    link = links[0]

    recipe_url = link.get('href')
    recipe_page = requests.get(recipe_url)

    recipe_soup = BeautifulSoup("%s" %(recipe_page.content), "html.parser")
    ingredient_section = recipe_soup.findAll("section", {"class": "component recipe-ingredients-new container"})
    
    if len(ingredient_section) == 0:
      ingredient_section = recipe_soup.findAll("section", {"class": "recipe-ingredients"})
      ingredient_soup = BeautifulSoup("%s" %(ingredient_section[0]), "html.parser")
      serving = 1
      ingredient_elements = ingredient_soup.findAll("span", {"class": "recipe-ingred_txt"})
    else:
      ingredient_soup = BeautifulSoup("%s" %(ingredient_section[0]), "html.parser")
      serving = int(ingredient_soup.find('div', class_='recipe-adjust-servings__size-quantity').text)
      ingredient_elements = ingredient_soup.findAll("span", {"class": "ingredients-item-name"})

    for ingredient_element in ingredient_elements:
      text = ingredient_element.text
      ingredient = text.replace('\\n', '')
      ingredient_text = ingredient.strip()

      if len(ingredient_text) > 1:
        ingredients.append(ingredient_text)

    image_section = recipe_soup.findAll("aside", {"class": "primary-media-section"})

    if len(image_section) == 0:
      image_section = recipe_soup.findAll("div", {"class": "hero-photo__wrap"})
      image_section_soup = BeautifulSoup("%s" %(image_section[0]), "html.parser")
      image = image_section_soup.find('img')
    else:
      image_section_soup = BeautifulSoup("%s" %(image_section[0]), "html.parser")
      image = image_section_soup.find('img')

    directions_elements = recipe_soup.findAll("li", {"class": "instructions-section-item"})

    if len(directions_elements) == 0:
      directions_elements = recipe_soup.findAll("span", {"class": "recipe-directions__list--item"})

      for directions_element in directions_elements:
        direction_text = directions_element.text

        if len(direction_text) > 1:
          directions.append(direction_text)
    else:
      for directions_element in directions_elements:
        direction_soup = BeautifulSoup("%s" %(directions_element), "html.parser")
        direction_text = direction_soup.find('p').text

        if len(direction_text) > 1:
          directions.append(direction_text)

    return SearchTerm(ingredients, serving, image['src'], directions)

class SearchTerm:
  def __init__(self, ingredients, serving, image, directions):
    self.ingredients = ingredients
    self.serving = serving
    self.image = image
    self.directions = directions
