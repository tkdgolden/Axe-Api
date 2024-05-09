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

  static async request(endpoint, data = {}, method = "get") {
    console.log("API Call:", endpoint, data, method);

    //there are multiple ways to pass an authorization token, this is how you pass it in the header.
    //this has been provided to show you another way to pass the token. you are only expected to read this code for this project.
    const url = `${BASE_URL}/${endpoint}`;
    const params = (method === "get")
      ? data
      : {};

    try {
      return (await axios({ url, method, data, params })).data;
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
      if (res.success === "true") {
        return true;
      }
      else return false;
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
      let res = await this.request('auth/register', data, "post");
      AxeApi.token = res.token;
      localStorage.token = res.token;
      return res;
    }
    catch (e) {
      return redirect("/login");
    }
  }

}

export default AxeApi;