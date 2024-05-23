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
      let res = await this.request('scores/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async allSeasons() {
    try {
      let res = await this.request('seasons/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async allTournaments() {
    try {
      let res = await this.request('tournaments/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async allPlayers() {
    try {
      let res = await this.request('competitors/all');
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async searchPlayers(playerName) {
    try {
      let res = await this.request(`competitors/${playerName}`)
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async getSeason(season_id) {
    try {
      let res = await this.request(`stats/season/${season_id}`);
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async getDiscipline(discipline) {
    try {
      let res = await this.request(`stats/discipline/${discipline}`);
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async getPlayer(playerId) {
    try {
      let res = await this.request(`stats/competitor/${playerId}`);
      return res;
    }
    catch (e) {
      return false;
    }
  }

  static async createSeason(data) {
    try {
      let res = await this.request('seasons', data, "post");
      return true;
    }
    catch {
      return false;
    }
  }

  static async createTournament(data) {
    try {
      let res = await this.request('tournaments', data, "post");
      return true;
    }
    catch {
      return false;
    }
  }

  static async seasonInfo(seasonId) {
    try {
      let res = await this.request(`seasons/${seasonId}`);
      return res;
    }
    catch {
      return false;
    }
  }

  static async createPlayer(playerData) {
    try {
      let id = await this.request('competitors', playerData, "post");
      return id;
    }
    catch {
      return false;
    }
  }

  static async enrollPlayer(playerId, seasonId=null, tournamentId=null) {
    const data = {
      competitor_id: playerId,
      season_id: seasonId,
      tournament_id: tournamentId
    }
    try {
      let res = await this.request('enrollment', data, "post");
      return res;
    }
    catch {
      return false;
    }
  }

  static async lapMatches(lapId) {
    try {
      let res = await this.request(`laps/${lapId}`);
      return res;
    }
    catch {
      return false;
    }
  }

  static async newLap(seasonId) {
    const data = {
      season_id: seasonId,
      discipline: 'hatchet'
    }
    try {
      let res = await this.request('laps', data, 'post');
      return res;
    }
    catch {
      return false;
    }
  }


  static async newMatch(p1Id, p2Id, lapId) {
    const data = {
      player_1_id: p1Id,
      player_2_id: p2Id,
      lap_id: lapId
    }
    try {
      let res = await this.request('matches', data, 'post');
      return res;
    }
    catch {
      return false;
    }
  }


  static async getMatch(matchId) {
    try {
      let res = await this.request(`matches/${matchId}`);
      return res;
    }
    catch {
      return false;
    }
  }


  static async submitMatch(data) {
    try {
      let matchRes = await this.request(`matches/${data.p1.match_id}`, data.match, "patch");
      let p1Res = await this.request('scores', data.p1, "post");
      let p2Res = await this.request('scores', data.p2, "post");
      return [matchRes, p1Res, p2Res];
    }
    catch {
      return false;
    }
  }


}

export default AxeApi;