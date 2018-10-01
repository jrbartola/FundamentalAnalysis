import { Injectable } from '@angular/core';

import {HttpClient, HttpErrorResponse, HttpHeaders, HttpParams} from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { GETResponse } from './response-structs';
import { Stock } from './stock';
import { EPS } from './eps';
import { DataPoint } from "./datapoint";
import { Revenue } from "./revenue";

@Injectable({
  providedIn: 'root'
})
export class StockService {

  constructor(private http: HttpClient) { }

  private stocksUrl: string = 'http://localhost:5000/api/stocks';  // URL to stock API
  private epsURL: string = 'http://localhost:5000/api/eps';        // URL to earnings API
  private revenueURL: string = 'http://localhost:5000/api/revenue';// URL to revenues API
  private dataUrl: string = 'https://api.iextrading.com/1.0/stock/{}/chart/5y';

  private emptyStock: Stock = {ticker: 'Stock Not Found', name: '', margin: null, sticker: null,
                               avgEpsGrowth: null, qoqEpsGrowth: null, avgSalesGrowth: null, qoqSalesGrowth: null};

  /**
   * Creates a set of headers compatible with CORS
   * @returns {Headers}
   */
  private static makeHeaders() {
    let headers = new HttpHeaders();
    headers.append('Access-Control-Allow-Credentials', 'true');
    headers.append('Access-Control-Allow-Methods', 'GET');
    headers.append('Access-Control-Allow-Origin', '*');
    return headers;
  }

  /**
   * Handle Http operation that failed.
   * Let the app continue.
   * @param operation - name of the operation that failed
   * @param result - optional value to return as the observable result
   */
  private handleError<T>(operation = 'operation', result?: T) {
    return (err: HttpErrorResponse): Observable<T> => {

      // TODO: send the error to remote logging infrastructure
      console.error(err.error.message);

      // Let the app keep running by returning an empty result.
      return of(result as T);
    };
  }

  /** GET stock by ticker. Will 404 if id not found */
  getStock(ticker: string, refresh: Boolean = false): Observable<Stock> {
    const headers = StockService.makeHeaders();
    let url = `${this.stocksUrl}/${ticker}`;
    url = refresh ? url + '?update=true' : url;

    return this.http.get<GETResponse<Stock>>(url, {headers: headers}).pipe(
      map(resp => resp.data),
      tap(resp => console.log(`Got stock with ticker: ${ticker}`, resp)),
      catchError((err: HttpErrorResponse) => {
        // If we receive a 404 and haven't refreshed the data, try fetch stock information
        if (err.status == 404 && !refresh) {
          return this.getStock(ticker, true);
        } else {
          return this.handleError<Stock>(`getStockOrUpdate ticker=${ticker}`, this.emptyStock)(err);
        }
      })
    );
  }

  /** GET Stocks from the server */
  getStocks(): Observable<Stock[]> {
    return this.http.get<Stock[]>(this.stocksUrl)
      .pipe(
        tap(_ => console.log(`fetched all stocks`)),
        catchError(this.handleError('getStocks', []))
      );
  }

  /** PUT: update the Stock on the server */
  updateStock(stock: Stock): Observable<any> {
    // Define the headers for our http request
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };
    return this.http.put(this.stocksUrl, Stock, httpOptions).pipe(
      tap(_ => console.log(`updated Stock id=${stock.ticker}`)),
      catchError(this.handleError<any>('updateStock'))
    );
  }

  /** POST: add a new Stock to the server */
  addStock(stock: Stock): Observable<Stock> {
    // Define the headers for our http request
    const httpOptions = {
      headers: new HttpHeaders({ 'Content-Type': 'application/json' })
    };

    return this.http.post<Stock>(this.stocksUrl, stock, httpOptions).pipe(
      tap((Stock: Stock) => console.log(`added Stock w/ ticker=${stock.ticker}`)),
      catchError(this.handleError<Stock>('addStock'))
    );
  }

  /** GET Stocks whose name contains search term */
  searchStocks(ticker: string): Observable<Stock> {
    if (!ticker.trim()) {
      return of(this.emptyStock);
    }
    return this.getStock(ticker);
  }

  getData(ticker: string, filter?: any): Observable<DataPoint[]> {
    return this.http.get<DataPoint[]>(this.dataUrl.replace("{}", ticker))
      .pipe(
        map((dataPoints) => {
          return dataPoints.map((d) => {
            d.date = new Date(d.date);
            return d;
          })
        })
      );
  }

  /** GET earnings by stock ticker. */
  getStockEarnings(ticker: string): Observable<EPS[]> {
    const headers = StockService.makeHeaders();
    let url = `${this.epsURL}/${ticker}`;

    return this.http.get<GETResponse<EPS[]>>(url, {headers: headers}).pipe(
        map(resp => resp.data),
        catchError(this.handleError<EPS[]>(`getStockEarnings ticker=${ticker}`, []))
    );
  }

  /** GET revenues by stock ticker. */
  getStockRevenues(ticker: string): Observable<Revenue[]> {
    const headers = StockService.makeHeaders();
    let url = `${this.revenueURL}/${ticker}`;

    return this.http.get<GETResponse<Revenue[]>>(url, {headers: headers}).pipe(
        map(resp => resp.data),
        catchError(this.handleError<Revenue[]>(`getStockRevenue ticker=${ticker}`, []))
    );
  }
}
