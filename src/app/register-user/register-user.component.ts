import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register-user',
  templateUrl: './register-user.component.html',
  styleUrls: ['./register-user.component.css']
})
export class RegisterUserComponent {
  signupUsers:any[]=[];
  signupObj: any={
    username:'',
    email:'',
    password:''
  };
  loginObj:any={
    username:'',
    password:''
  };

  constructor(private router: Router){ }

  ngOnInit(): void{
    const localData=localStorage.getItem('signUpUsers');
    if(localData!=null){
      this.signupUsers=JSON.parse(localData);
    }
    this.signupObj={
      username:'',
      email:'',
      password:''
    };
  }

  onSignUp(){
    if(this.signupObj.username!="" && this.signupObj.email!="" && this.signupObj.password!=""){
      this.signupUsers.push(this.signupObj);
      alert("Successfully signed up....Now login to continue");
    }
    
    localStorage.setItem('signUpUsers',JSON.stringify(this.signupUsers));
    
  }
  onLogin():void{
    const isUserExist= this.signupUsers.find(m=>m.username==this.loginObj.username && m.password==this.loginObj.password);
    if(isUserExist!=undefined){
      this.router.navigateByUrl('/mainpage');
    }else{
      alert("Wrong credentials");
    }
    

  }
}
