import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms'; // <-- NgModel lives here
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppComponent } from './app.component';
import { AppRoutingModule } from './/app-routing.module';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HttpClientModule, HttpClientJsonpModule } from "@angular/common/http";
import { StockSearchComponent } from './stock-search/stock-search.component';
import { NavbarComponent } from './navbar/navbar.component';

import { MaterialModule } from './material.module';
import { StockDetailComponent } from './stock-detail/stock-detail.component';
import { StockChartComponent } from './stock-chart/stock-chart.component';
import { ChartsModule } from '@progress/kendo-angular-charts';
import 'hammerjs';
import { MatDialogModule } from "@angular/material";
import { InfoDialogComponent } from './info-dialog/info-dialog.component';



@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    StockSearchComponent,
    NavbarComponent,
    StockDetailComponent,
    StockChartComponent,
    InfoDialogComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    FormsModule,
    AppRoutingModule,
    HttpClientModule,
    HttpClientJsonpModule,
    MaterialModule,
    ChartsModule,
    MatDialogModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [InfoDialogComponent]

})
export class AppModule { }
