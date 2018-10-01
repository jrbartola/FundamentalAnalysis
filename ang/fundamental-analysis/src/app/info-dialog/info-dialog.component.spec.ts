import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { MatDialogModule } from "@angular/material";

import { InfoDialogComponent } from './info-dialog.component';
import { MaterialModule } from '../material.module';

describe('InfoDialogComponent', () => {
  let component: InfoDialogComponent;
  let fixture: ComponentFixture<InfoDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ MatDialogModule, MaterialModule ],
      declarations: [ InfoDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InfoDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
