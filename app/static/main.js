const { createApp } = Vue

const NRApp = {
    data() {
        return {
            userID: "",
            newsID: "",
            page: 'news-rs',
            newsList: [],
            usersList: [],
            readByUserList: [],
            randomNewsList: [],
            newUserID: ""
        }
    },
    async created() {
        //await this.getNews('U169207')
    },
    methods: {
        async sendRequest(url, method, data) {
            const myHeaders = new Headers({
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            })

            const response = await fetch(url, {
                method: method,
                headers: myHeaders,
                body: data
            })

            return response
        },
        async getNews(userID) {
            console.log(JSON.stringify(userID))
            // const response = await this.sendRequest(window.location + 'get-news', 'post', JSON.stringify(userID))
            await this.sendRequest(window.location + 'get-news', 'post', JSON.stringify(userID)).then((response) => response.json()).then((newsArray) => {
                console.log(newsArray);
                this.newsList = [];
                for(let i=0; i<newsArray.length; i++) {
                    let news = {};
                    news.entity = newsArray[i][0];
                    news.id = newsArray[i][1];
                    news.title = newsArray[i][2];
                    news.abstract = newsArray[i][3];
                    news.relatedNewsID = newsArray[i][4];
                    news.relatedNewsTitle = newsArray[i][5];
                    this.newsList.push(news);
                }
                console.log(this.newsList)
            })
            // const response = await this.sendRequest(window.location, 'get')

            // const response = await fetch(window.location, {
            //     method: 'get',
            //     headers: {
            //         'X-Requested-With': 'XMLHttpRequest'
            //     }
            // })

            // this.newsList = response.json() // variavel que vai iterar o for na lista de noticias no vue
            // responseJson = response.json()
            // console.log(responseJson)
            // this.newsList = [];
            // for(let i=0; i<response.length; i++) {
            //     console.log(i);
            //     news = {}
            //     news.entity = response[i][0];
            //     news.id = response[i][1];
            //     news.title = response[i][2];
            //     news.abstract = response[i][3];
            //     news.relatedNewsTitle = response[i][4];
            //     news.relatedNewsAbstract = response[i][5];
            //     this.newsList.push(news);
            // }
            // console.log(this.newsList);
        },
        // async readNews(newsID) {
        //     await this.getNews()

        //     await this.sendRequest(window.location + 'read-news', 'post', JSON.stringify(newsID))

        //     // const response = await fetch(window.location + 'newsRead', {
        //     //     method: 'post',
        //     //     headers: {
        //     //         'Content-Type': 'application/json',
        //     //         'X-Requested-With': 'XMLHttpRequest'
        //     //     },
        //     //     body: JSON.stringify(newsID)
        //     // })

        //     await this.getNews()
        // }
        async getUsers(newsID) {
            console.log(JSON.stringify(newsID))
            await this.sendRequest(window.location + 'get-users', 'post', JSON.stringify(newsID)).then((response) => response.json()).then((usersArray) => {
                console.log(usersArray);
                this.usersList = [];
                for(let i=0; i<usersArray.length; i++) {
                    let user = {};
                    //e.label, n2.id, n2.title, u2.id
                    user.entity = usersArray[i][0];
                    user.relatedNewsID = usersArray[i][1];
                    user.relatedNewsTitle = usersArray[i][2];
                    user.id = usersArray[i][3];
                    this.usersList.push(user);
                }
                console.log(this.usersList)
            })
        },
        async readNews(newsID, userID) {
            let time = new Date()
            let obj = {
                newsID: newsID,
                userID: userID,
                time: time.toString(),
            }
            await this.sendRequest(window.location + 'read-news', 'post', JSON.stringify(obj))
        },

        async getReadByUser(userID) {
            await this.sendRequest(window.location + 'get-read-by-user', 'post', JSON.stringify(userID)).then((response) => response.json()).then((newsArray) => {
                this.readByUserList = [];
                for(let i=0; i<newsArray.length; i++) {
                    let news = {};
                    news.id = newsArray[i][0];
                    news.title = newsArray[i][1];
                    news.entities = newsArray[i][2].toString();
                    this.readByUserList.push(news);
                }
            })
        },

        async createUser(userID) {
            await this.sendRequest(window.location + 'create-user', 'post', JSON.stringify(userID))
        },

        async getRandomNews() {
            await this.sendRequest(window.location + 'get-random-news', 'post', "").then((response) => response.json()).then((newsArray) => {
                this.randomNewsList = [];
                for(let i=0; i<newsArray.length; i++) {
                    let news = {};
                    news.id = newsArray[i][0];
                    news.title = newsArray[i][1];
                    news.entities = newsArray[i][2].toString();
                    this.randomNewsList.push(news);
                }
            })
        },

        removeFromNewsList(newsID) {
            this.readNews(newsID, this.userID);
            this.newsList = this.newsList.filter(function( news ) {
                return news.id !== newsID;
            });
        },

        removeFromRandomNewsList(newsID) {
            this.createUser(this.newUserID);
            this.readNews(newsID, this.newUserID);
            this.randomNewsList = this.randomNewsList.filter(function( news ) {
                return news.id !== newsID;
            });
        }
    },
    delimiters: ['{', '}']
}

createApp(NRApp).mount('#app')