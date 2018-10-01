import { Component, OnInit } from '@angular/core';
import {Stock} from "../stock";
import {Observable, of} from "rxjs/index";

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: [ './dashboard.component.css' ]
})
export class DashboardComponent implements OnInit {
  public stock: Stock;

  constructor() {

  }

  ngOnInit() {
    this.stock = {ticker: 'No Stock Selected', name: '', margin: null, sticker: null,
                  avgEpsGrowth: null, qoqEpsGrowth: null, avgSalesGrowth: null, qoqSalesGrowth: null};
  }
}
