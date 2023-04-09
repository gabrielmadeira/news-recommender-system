from neo4j import GraphDatabase

class MindKG:
    driver = None
    url = None
    user = None
    password = None

    def __init__(self, url, user, password):
        self.url = url
        self.user = user
        self.password = password

    def connect(self):
        self.driver = GraphDatabase.driver(self.url, auth=(self.user, self.password))
    def close(self):
        self.driver.close()

    @staticmethod
    def recommendNewsQuery(tx, userID):
        result = tx.run("MATCH path = (u:User {id: $userID})-[read:READ]->(n:News)-[content:CONTENT]->(e:Entity)-[content2:CONTENT]->(n2:News) "
                        "WHERE n2.id <> n.id "
                        "WITH e, n, n2, rand() AS rnd "
                        "WITH e, n, n2, collect(rnd)[0..1] AS rnd " # collect(n2) AS nn, collect(n2.id) AS n2ic, collect(n2.title) AS n2tc, collect(n2.abstract) AS n2ac,
                        "RETURN e.label, n2.id, n2.title, n2.abstract, n.id, n.title ORDER BY rnd LIMIT 10", userID=userID)
        return list(result)

    @staticmethod
    def recommendUsersQuery(tx, newsID):
        result = tx.run("MATCH path = (n:News{id: $newsID})-[content:CONTENT]-(e:Entity)-[content2:CONTENT]-(n2:News)-[read2:READ]-(u2:User) "
                        "WHERE n2.id <> n.id "
                        "WITH e, n2, u2, rand() AS rnd "
                        "WITH e, n2, u2, collect(rnd)[0..1] AS rnd "
                        "RETURN e.label, n2.id, n2.title, u2.id AS user ORDER BY rnd LIMIT 20", newsID=newsID)
        return list(result)
    
    @staticmethod
    def connectUserToNewsQuery(tx, userID, newsID, time):
        result = tx.run("MATCH (u:User), (n:News) "
                        "WHERE u.id=$userID AND n.id=$newsID "
                        "MERGE (u)-[rd1:READ]->(n) "
                        "MERGE (n)-[rd2:READ]->(u) "
                        "SET rd1.time=$time "
                        "SET rd2.time=$time ", userID=userID, newsID=newsID, time=time)
        return result

    @staticmethod
    def createUserQuery(tx, ID, new): #new/last acess
        result = tx.run("MERGE (a:User{id: $ID, new:$new}) ", ID=ID, new=new)
        return result

    @staticmethod
    def readByUserQuery(tx, userID):
        result = tx.run("MATCH (u:User{id: $userID})-[r:READ]->(n:News)-[c:CONTENT]->(e:Entity) RETURN n.id, n.title, collect(e.label) ", userID=userID)
        return list(result)

    @staticmethod
    def randomNewsQuery(tx):
        result = tx.run("MATCH (n:News)-[c:CONTENT]->(e:Entity) "
                        "WITH n, e, rand() AS rnd "
                        "WITH n, collect(e.label) AS entities, collect(rnd)[0..1] AS rnd "
                        "RETURN n.id, n.title, entities "
                        "ORDER BY rnd LIMIT 15 ") 
        return list(result)


    def getNews(self, userID):
        with self.driver.session() as session:
            newsList = session.execute_read(self.recommendNewsQuery, userID)
            #for news in newsList: 
            #    print(news.get("e.label") + " - " + news.get("n2.id") + " - " + news.get("n2.title") + "\n\n\t" + news.get("n2.abstract") + "\n\n\n") # news.data() news.get("n2c[0]")
            return newsList

    def getUsers(self, newsID):
        with self.driver.session() as session:
            userList = session.execute_read(self.recommendUsersQuery, newsID)
            # for user in userList: 
            #     print(news.get("e.label") + " - " + news.get("u2.id") )
            return userList
        
    def readNews(self, userID, newsID, time):
        with self.driver.session() as session:
            result = session.execute_write(self.connectUserToNewsQuery, userID, newsID, time)
            return "Ok"

    def createUser(self, userID):
        with self.driver.session() as session:
            session.execute_write(self.createUserQuery, userID, '1')
            return "Ok"

    def getReadByUser(self, userID):
        with self.driver.session() as session:
            newsList = session.execute_read(self.readByUserQuery, userID)
            return newsList

    def getRandomNews(self):
        with self.driver.session() as session:
            newsList = session.execute_read(self.randomNewsQuery)
            return newsList
