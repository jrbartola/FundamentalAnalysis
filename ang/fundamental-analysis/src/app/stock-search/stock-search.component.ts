import {Component, EventEmitter, Input, OnInit, Output, SimpleChanges} from '@angular/core';
import {MatDialog, MatDialogConfig} from "@angular/material";

import { Observable, Subject } from 'rxjs';

import {
   debounceTime, distinctUntilChanged, switchMap
 } from 'rxjs/operators';

import { Stock } from '../stock';
import { StockService } from '../stock.service';
import {tap} from "rxjs/internal/operators";
import {InfoDialogComponent} from "../info-dialog/info-dialog.component";

@Component({
  selector: 'app-stock-search',
  templateUrl: './stock-search.component.html',
  styleUrls: [ './stock-search.component.css' ]
})
export class StockSearchComponent implements OnInit {
  @Input() stock: Stock;
  @Output() stockChange = new EventEmitter();

  private loading: boolean = false;
  private searchTerms = new Subject<string>();

  constructor(private stockService: StockService, private dialog: MatDialog) {}

  // Push a search term into the observable stream.
  search(term: string): void {
    this.loading = true;
    this.searchTerms.next(term);
  }

  ngOnInit(): void {
    this.searchTerms.pipe(
      // wait 300ms after each keystroke before considering the term
      debounceTime(300),

      // ignore new term if same as previous term
      distinctUntilChanged(),

      // switch to new search observable each time the term changes
      switchMap((term: string) => this.stockService.searchStocks(term)),
    ).subscribe((stock) => {
                   this.loading = false;
                   if (!stock.name) {
                     // If there was no stock that resulted, show the error dialog.
                     this.launchDialog();
                     return;
                   }
                   this.stock = stock;
                   this.stockChange.emit(stock);

                 },
                err => console.log(err),
                () => console.log("Channel closed."));
  }

  ngOnChanges(changes: SimpleChanges) {
    if (this.stock.name) {
      if (this.stock.avgEpsGrowth) {
        this.stock.avgEpsGrowth /= 100.0;
      }
      if (this.stock.avgSalesGrowth) {
        this.stock.avgSalesGrowth /= 100.0;
      }
    }
  }

  launchDialog() {
    const dialogConfig = new MatDialogConfig();
    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    this.dialog.open(InfoDialogComponent, dialogConfig);
  }
}
