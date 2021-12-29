import random

# generate data
sample_len = 10000

movies_list = ['id_' + str(x) for x in random.sample(range(1, 20000), sample_len)]
similar_movies = [random.sample(movies_list, 2) for _ in range(sample_len // 2)]
friends_seen_movies = [random.sample(movies_list, random.randint(0, 2000)) for _ in range(8000)]
# end of data generating

movie_to_friends_seen = dict()

for movies in friends_seen_movies:
    for movie in movies:
        movie_to_friends_seen[movie] = movie_to_friends_seen.get(movie, 0) + 1

similarity_graph = dict()

for left, right in similar_movies:
    if left in similarity_graph:
        similarity_graph[left].append(right)
    else:
        similarity_graph[left] = [right]
    if right in similarity_graph:
        similarity_graph[right].append(left)
    else:
        similarity_graph[right] = [left]

num_of_friends = len(friends_seen_movies)
best_film = None
best_result = 0

for film in movie_to_friends_seen:
    F = movie_to_friends_seen[film]
    similar_films = dict()

    def dfs(v):
        similar_films[v] = True
        for u in similarity_graph[v]:
            if u not in similar_films:
                dfs(u)
    if film in similarity_graph:
        dfs(film)

    if len(similar_films) == 0:
        continue
    else:
        sum_of_sim_films = 0
        for similar_film in similar_films:
            if similar_film in movie_to_friends_seen:
                sum_of_sim_films += movie_to_friends_seen[similar_film]
        S = sum_of_sim_films / num_of_friends

    result = F / S

    if result > best_result:
        best_result = result
        best_film = film

print(best_film)
