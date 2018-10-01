import {Component, EventEmitter, Input, OnInit, Output, SimpleChanges} from '@angular/core';

import {HexHelpers} from "../style-utils";
import {Stock} from "../stock";
import {StockService} from "../stock.service";

@Component({
  selector: 'app-stock-detail',
  templateUrl: './stock-detail.component.html',
  styleUrls: ['./stock-detail.component.css']
})
export class StockDetailComponent implements OnInit {
  @Input() stock: Stock;
  @Output() stockChange = new EventEmitter();

  private loading: boolean = false;
  private qoqEpsLabelColor: string;
  private avgEpsLabelColor: string;
  private qoqRevenueLabelColor: string;
  private avgRevenueLabelColor: string;

  private setLabelColors(): void {
    this.qoqEpsLabelColor = HexHelpers.calculateColorGradient(this.stock.qoqEpsGrowth, 0.0, 0.25,
                                                              '#ff0000', '#008000')
    this.avgEpsLabelColor = HexHelpers.calculateColorGradient(this.stock.avgEpsGrowth, 0.0, 0.25,
                                                              '#ff0000', '#008000')
    this.qoqRevenueLabelColor = HexHelpers.calculateColorGradient(this.stock.qoqSalesGrowth, 0.0, 0.25,
                                                              '#ff0000', '#008000')
    this.avgRevenueLabelColor = HexHelpers.calculateColorGradient(this.stock.avgSalesGrowth, 0.0, 0.25,
                                                              '#ff0000', '#008000')
  }

  constructor(private stockService: StockService) {}

  ngOnInit() {

  }

  ngOnChanges(changes: SimpleChanges) {
    if (this.stock.name) {
      this.setLabelColors();
    }
  }

  refreshData() {
    // Don't send a request if there is no Stock in view to update
    if (!this.stock.name)
      return;

    this.loading = true;
    this.stockService.getStock(this.stock.ticker, true)
      .subscribe((stock) => {
         this.stock = stock;
         this.stockChange.emit(stock);
         this.loading = false;
      })
  }

}
