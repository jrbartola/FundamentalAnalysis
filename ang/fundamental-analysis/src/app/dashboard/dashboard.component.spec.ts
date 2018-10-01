import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientModule } from "@angular/common/http";
import { ChartsModule } from "@progress/kendo-angular-charts";

import { DashboardComponent } from './dashboard.component';
import { MaterialModule } from "../material.module";
import { StockSearchComponent } from "../stock-search/stock-search.component";
import { StockChartComponent } from "../stock-chart/stock-chart.component";
import { StockDetailComponent } from "../stock-detail/stock-detail.component";

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ HttpClientModule, MaterialModule, ChartsModule ],
      declarations: [ DashboardComponent, StockSearchComponent, StockChartComponent, StockDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
