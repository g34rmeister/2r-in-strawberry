import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
    leaderboardURL:"http://localhost:8000/api/userdata/global-leaderboard/",
    withCredentials: true,

})

export default api
