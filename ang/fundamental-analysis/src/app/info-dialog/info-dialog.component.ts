import {Component, Inject, Input, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material";

@Component({
  selector: 'app-info-dialog',
  templateUrl: './info-dialog.component.html',
  styleUrls: ['./info-dialog.component.css']
})
export class InfoDialogComponent implements OnInit {
  @Input() ticker: string;

  constructor(private dialogRef: MatDialogRef<InfoDialogComponent>) {
  }

  ngOnInit() {
  }

  close() {
    this.dialogRef.close();
  }

}
