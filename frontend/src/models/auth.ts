export interface Token {
  /**
   * Frontend model for the Token
   * @returns access token and return token type
   */
  access_token: string;
  token_type: string;
}

export interface TokenJSON {
  /**
   * Response Model for the Token
   * @returns access token and token type
   */
  access_token: string;
  token_type: string;
}

export interface TokenData {
  /**
   * Frontend Model for the Token Data
   * @returns id, name of the token, and expiration date of the token
   */
  id: number;
  name: number;
  expiration_time: string;
}

export interface TokenDataJSON {
  /**
   * Response Model for the Token Data
   * @returns access token and token type
   */
  id: number;
  name: number;
  expiration_time: string;
}

export interface Login {
  /**
   * Frontend Model for the Login Data
   */
  name: string;
  password: string;
}
