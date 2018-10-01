/** response-structs.ts contains interfaces that capture the shape of HTTP responses **/

export interface GETResponse<T> {
  data: T;
  status: string;
}
