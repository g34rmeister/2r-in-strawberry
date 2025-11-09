import axios from "axios";

import {ACCESS_TOKEN, REFRESH_TOKEN} from "./LocalStorage"

//Create api object and default link for it to backend.
const api = axios.create({
    baseURL: 'http://localhost:8000/api/',
})

//Set up interceptor for outbound requests
api.interceptors.request.use(
    //This function is run during the request. Config if just the object going outs configuraiton like headers
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        //If we have a token then attach token
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config//Return modified request. Can either have or not have the token
    },
    //Run if there was an error
    (error) => {
        return Promise.reject(error)//Make error availible to catch of whatever called this interceptor
    }
)

//set up interceptor for inbound requests
api.interceptors.response.use(
    (response) => {
        console.log("Valid access token used");
        return response;
    },//Normal success so just return the response as is
    //Error occured so check token refresh
    async (error) => {
        const ogRequest = error.config;//Origional request sent before the response

        //Check for 401 (unautorized) or if we have already intercepted this response
        if (error.response.status === 401 && !ogRequest._retry) {
            ogRequest._retry = true//Mark response as already taken once
            //User was unauthorized so try to refresh token

            try {
                const refToken = localStorage.getItem(REFRESH_TOKEN);
                const response = await axios.post(`${import.meta.env.VITE_API_URL_FOR_TEST}/token/refresh`, {refresh: refToken});//Try to refresh token
                
                //Success so send another request
                const { access } = response.data;
                localStorage.setItem(ACCESS_TOKEN, access);

                //Update key for request
                ogRequest.headers.Authorization = `Bearer ${access}`;

                //Send response back for a second time and return its response
                console.log("Got new token from refresh!");
                return api(ogRequest);
            } catch (refError) {
                //Failed to get new token. Refresh token most likely expired.
                console.error("Attempt to refresh token failed!");
                localStorage.removeItem(ACCESS_TOKEN);
                localStorage.removeItem(REFRESH_TOKEN);
                //Return error
                return Promise.reject(refError)
            }
        }
        //Normal error
        return Promise.reject(error)
    }
)

export default api