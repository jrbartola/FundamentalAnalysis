import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientModule } from "@angular/common/http";
import { MatDialogModule } from "@angular/material";
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { StockSearchComponent } from './stock-search.component';
import { MaterialModule } from "../material.module";


describe('StockSearchComponent', () => {
  let component: StockSearchComponent;
  let fixture: ComponentFixture<StockSearchComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StockSearchComponent ],
      imports: [ HttpClientModule, MaterialModule, MatDialogModule, BrowserAnimationsModule ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StockSearchComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
