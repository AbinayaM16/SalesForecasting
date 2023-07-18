import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {MainpageComponent} from '../app/mainpage/mainpage.component'
import { RegisterUserComponent } from './register-user/register-user.component';

const routes: Routes = [
  {
    path:'', component:RegisterUserComponent
  },
  {
    path:'mainpage', component:MainpageComponent},
  
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
