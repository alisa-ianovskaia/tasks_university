from imdb_helper_functions import *
import time

domain = 'https://www.imdb.com'


def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    """ Takes a BeautifulSoup object as first arg, limit of output values as second (unnecessary)
        Returns list of pairs (actors name, link to his page)
    """
    if cast_page_soup:
        actors_list = list()
        cast_soup_links = cast_page_soup.select('table.cast_list td.primary_photo + td a')

        if num_of_actors_limit and num_of_actors_limit < len(cast_soup_links):
            limit = num_of_actors_limit
        else:
            limit = len(cast_soup_links)

        for el in range(limit):
            name = cast_soup_links[el].text.strip()
            url = domain + cast_soup_links[el]['href']

            actors_list.append((name, url))

        return actors_list
    return []


def get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit=None):
    """ Takes a BeautifulSoup object as first arg, limit of output values as second (unnecessary)
        Returns list of pairs (film name, link to its page)
    """
    if actor_page_soup:
        films_list = list()

        try_actor = actor_page_soup.find(id='filmo-head-actor')
        actors_section = try_actor if try_actor else actor_page_soup.find(id='filmo-head-actress')

        if actors_section:
            films_soup = actors_section.find_next_sibling('div').select('.filmo-row')

            for film in films_soup:
                link = film.find('b')
                text_after_link = link.next_sibling
                if text_after_link == '\n':
                    url = domain + link.find('a')['href'] + 'fullcredits'
                    films_list.append((link.text, url))

            return films_list[:num_of_movies_limit] if num_of_movies_limit else films_list
    return []


def get_movie_distance(actor_start_url, actor_end_url, num_of_actors_limit=None, num_of_movies_limit=None):
    ''' Receives two urls of actors' pages, returns the number of films (distance)
        between them
    '''
    distance = 1
    max_distance = 3

    # build dictionaries from cached data
    file_films = 'films_data.json'
    file_actors = 'actors_data.json'
    cached_films = get_cached_data(file_films)
    cached_actors = get_cached_data(file_actors)

    page_actor_1 = get_html_page(actor_start_url)
    page_actor_2 = get_html_page(actor_end_url)

    start_actor_soup = get_soup(page_actor_1)
    end_actor_soup = get_soup(page_actor_2)

    start_actor_name = start_actor_soup.select('h1 span.itemprop')[0].text.strip()
    target_actor_name = end_actor_soup.select('h1 span.itemprop')[0].text.strip()

    # sets for actors and films that were already seen while processing
    seen_actors = set()
    seen_films = set()

    seen_actors.add(start_actor_name)

    # get films for both actors and check whether there is a common film
    films_1 = get_movies_by_actor_soup(start_actor_soup, num_of_movies_limit)
    films_2 = get_movies_by_actor_soup(end_actor_soup, num_of_movies_limit)

    if are_common_films(films_1, films_2):
        return distance

    # list of films of the first actor that we will check
    films_to_process = list(films_1)

    # list that will be filled with films of the next level
    next_films = list()

    while films_to_process and distance <= max_distance:
        current_film = films_to_process.pop()
        film_name = current_film[0]

        if not film_name in seen_films:
            # first try to get film data from cache
            if film_name in cached_films:
                current_film_page = cached_films[film_name]
            else:
                current_film_page = get_html_page(current_film[1])
                time.sleep(0.2)
                save_page_to_file(file_films, current_film_page, film_name)

            film_soup = get_soup(current_film_page)
            seen_films.add(film_name)

            actors_to_process = get_actors_by_movie_soup(film_soup, num_of_actors_limit)

            while actors_to_process:
                current_actor = actors_to_process.pop()
                actor_name = current_actor[0]

                if actor_name == target_actor_name:
                    return distance

                # we get films from actor only in case if it's not the last level
                if (not actor_name in seen_actors) and (distance < max_distance):
                    if actor_name in cached_actors:
                        # and first look in cache too
                        current_actor_page = cached_actors[actor_name]
                    else:
                        current_actor_page = get_html_page(current_actor[1])
                        time.sleep(0.2)
                        save_page_to_file(file_actors, current_actor_page, actor_name)

                    films_for_current_actor = get_movies_by_actor_soup(get_soup(current_actor_page),
                                                                       num_of_movies_limit)
                    seen_actors.add(actor_name)
                    next_films.extend(films_for_current_actor)

        # if there are no films in this level, increase distance by 1
        # and use films that were found from actors at this level
        if len(films_to_process) == 0:
            distance += 1
            films_to_process = next_films
            next_films = list()
            time.sleep(0.5)

    return float('inf')


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    # your code here
    return None
