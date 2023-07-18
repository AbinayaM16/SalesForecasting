
import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import 'firebase/auth';
import { Router } from '@angular/router';
@Component({
  selector: 'app-mainpage',
  templateUrl: './mainpage.component.html',
  styleUrls: ['./mainpage.component.css']
})
export class MainpageComponent{
  imageUrl!: string;

  public forecastPeriod!: string;
  public frequency!: string;
  public salesDataset!: File;

  constructor(private http: HttpClient,private router: Router) {
  }

  onFileSelected(event: any) {
    this.salesDataset = event.target.files[0];
  }

  onSubmit() {
    if (!this.salesDataset || !this.frequency || !this.forecastPeriod) {
      alert('Please fill in all required fields.');
      return;
    }
    const formData = new FormData();
    formData.append('salesDataset', this.salesDataset);
    formData.append('frequency', this.frequency);
    formData.append('forecastPeriod', this.forecastPeriod);
    this.http.post('http://localhost:5000/upload-csv', formData, { responseType: 'blob' }).subscribe(
      /*
      (response) => {
        console.log(response);
        console.log(response.forecast_data)
       
        // Store response in local storage
        localStorage.setItem('response', JSON.stringify(response));
      },
      */
      res => {
        const reader = new FileReader();
        reader.onload = (e: any) => {
          this.imageUrl = e.target.result;
        }
        reader.readAsDataURL(res);
      },
      (error) => {
        console.log(error);
        
      }
      
    );

  }
  
}
