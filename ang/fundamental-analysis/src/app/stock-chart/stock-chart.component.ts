import { Component, Input, SimpleChanges } from '@angular/core';
import { zip } from 'rxjs';
import { StockService } from '../stock.service';
import { Stock } from "../stock";
import { DataPoint } from "../datapoint";
import { EPS } from "../eps";

@Component({
    selector: 'app-stock-chart',
    templateUrl: './stock-chart.component.html',
    styleUrls: ['./stock-chart.component.css']
})
export class StockChartComponent {
    @Input() stock: Stock;

    public stockData: DataPoint[] = [];
    public epsData: number[] = [];
    public revenueData: number[] = [];
    public epsRevAxisLabels: Date[] = [];
    public epsRevCrossingValues: number[] = [-1, 0];

    public from: Date = new Date('2018/01/31');
    public to: Date = new Date();

    /**
     * Converts a timestamp in seconds since epoch to a locale date string
     * @param {number} epoch The epoch time in seconds
     * @returns {string} A locale date string of the form MM/DD/YYYY
     */
    private epochToDateString(epoch: number): Date {
      return new Date(epoch * 1000);
      // return d.toLocaleDateString();
    }

    constructor(private service: StockService) {
    }

    ngOnChanges(changes: SimpleChanges) {
      if (this.stock && this.stock.name) {
        this.createStockChart();
        this.createEarningsChart();
      } else {
        this.stockData = [];
        this.epsData = [];
      }
    }

    createStockChart() {
      this.service.getData(this.stock.ticker).subscribe((data) => {
        this.stockData = data;
      }, (err) => {
        console.error("Error occurred when getting timeseries data");
        console.error(err);
      });
    }

    createEarningsChart() {
      const ofEarnings = this.service.getStockEarnings(this.stock.ticker);
      const ofRevenues = this.service.getStockRevenues(this.stock.ticker);

      // Combine both observables and create the chart with both eps and revenue plotted
      zip(ofEarnings, ofRevenues).subscribe(([epsData, revData]) => {
        this.epsData = epsData.map(d => d.earnings);
        this.epsRevAxisLabels = epsData.map(d => this.epochToDateString(d.time));
        this.revenueData = revData.map(d => d.revenue);
        this.epsRevCrossingValues = [0, this.epsRevAxisLabels.length];
      }, (err) => {
        console.error("Error occurred when creating earnings chart");
        console.error(err);
      });
    }
}
