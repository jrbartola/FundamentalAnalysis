import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientModule } from "@angular/common/http";

import { ChartsModule } from '@progress/kendo-angular-charts';

import { StockChartComponent } from './stock-chart.component';
import { MaterialModule } from "../material.module";

describe('StockChartComponent', () => {
  let component: StockChartComponent;
  let fixture: ComponentFixture<StockChartComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StockChartComponent ],
      imports: [ MaterialModule, HttpClientModule, ChartsModule ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StockChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
