# Задание: система рекомендаций на основе общих интересов

class RecommendationSystem:
    def __init__(self):
        self.users = {}

    def add_user(self, username, interests):
        self.users[username] = set(interests)

    def common_interests(self, user1, user2):
        if user1 not in self.users or user2 not in self.users:
            return set()
        return self.users[user1] | self.users[user2]

    def similarity(self, user1, user2):
        common = self.common_interests(user1, user2)
        all_interests = self.users[user1] | self.users[user2]
        if not all_interests:
            return 0
        return len(common) / len(all_interests)

    def recommend(self, username, top_n=3):
        if username not in self.users:
            return []

        similarities = []
        for other_user in self.users:
            if other_user != username:
                sim = self.similarity(username, other_user)
                similarities.append((other_user, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_users = similarities[:top_n]

        recommendations = set()
        user_interests = self.users[username]
        for similar_user, _ in top_users:
            new_interests = self.users[similar_user] - user_interests
            recommendations.update(new_interests)

        return list(recommendations)

    def all_interests(self):
        all_int = set()
        for interests in self.users.values():
            all_int.update(interests)
        return all_int


rs = RecommendationSystem()
rs.add_user("Анна", ["Python", "ML", "математика", "шахматы"])
rs.add_user("Борис", ["Python", "веб", "JavaScript", "шахматы"])
rs.add_user("Виктор", ["ML", "математика", "статистика", "R"])
rs.add_user("Галина", ["Python", "ML", "статистика", "визуализация"])

print(f"Схожесть Анна-Борис: {rs.similarity('Анна', 'Борис'):.2f}")
print(f"Схожесть Анна-Виктор: {rs.similarity('Анна', 'Виктор'):.2f}")
print(f"Общие интересы Анна-Виктор: {rs.common_interests('Анна', 'Виктор')}")
print(f"Рекомендации для Анны: {rs.recommend('Анна')}")
