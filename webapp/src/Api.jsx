import axios from "axios";
import { redirect } from "react-router-dom";

const BASE_URL = import.meta.env.REACT_APP_BASE_URL || "http://localhost:5000";

/** API Class.
 *
 * Static class tying together methods used to get/send to to the API.
 * There shouldn't be any frontend-specific stuff here, and there shouldn't
 * be any API-aware stuff elsewhere in the frontend.
 *
 */

class AxeApi {
  static token;

  static async request(endpoint, data = {}, method = "get") {
    console.log("API Call:", endpoint, data, method);

    // can get token from local storage on page refresh without having to log back in
    if (!AxeApi.token) {
      AxeApi.token = localStorage.token;
    }

    //there are multiple ways to pass an authorization token, this is how you pass it in the header.
    //this has been provided to show you another way to pass the token. you are only expected to read this code for this project.
    const url = `${BASE_URL}/${endpoint}`;
    const headers = { Authorization: `${AxeApi.token}` };
    const params = (method === "get")
      ? data
      : {};

    try {
      return (await axios({ url, method, data, params, headers })).data;
    } catch (err) {
      console.error("API Error:", err.response);
      let message = err.response.data.error.message;
      throw Array.isArray(message) ? message : [message];
    }
  }
  

  // Individual API routes

  /**
   * logs in a user by verifying username and password to get a token and store that in AxeApi.token as well as on the localStorage
   * @param {object} data username and password
   * @returns true or false on success
   */
  static async login(data) {

    try {
      let res = await this.request('judges/verify', data, "post");
      AxeApi.token = res['token'];
      localStorage.token = res['token'];
      return true;
    }
    catch {
      return false;
    }
  }

  /**
   * registers a new user and saves the response token
   * @param {object} data { username, password }
   */
  static async register(data) {
    try {
      let res = await this.request('judges/new', data, "post");
      return res['success'];
    }
    catch (e) {
      return redirect("/register");
    }
  }

  static async overallStats() {
    try {
      let res = await this.request('/scores/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async allSeasons() {
    try {
      let res = await this.request('/seasons/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async getSeason(season_id) {
    try {
      console.log(season_id);
      let res = await this.request(`/seasons/${season_id}`);
      return res;
    }
    catch (e) {
      return false;
    }
  }

}

export default AxeApi;