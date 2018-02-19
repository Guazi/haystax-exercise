import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  rForm: FormGroup;
  post: any; // A property for our submitted form
  email: string = '';
  phone: string = '';
  password: string = '';
  titleAlert: string = 'This field is required';
  emailAlert: string = 'Please enter a valid email in the format name@domain.com';
  phoneAlert: string = 'Please enter in the format 202-595-4670';

  // set up the validation methods
  constructor(private fb: FormBuilder) {
    this.rForm = fb.group({
      email: [
        null,
        Validators.compose([
          Validators.required,
          Validators.pattern(/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/)
        ])
      ],
      password: [null, Validators.compose([Validators.required, Validators.minLength(8), Validators.maxLength(20)])],

      phone: [null, Validators.pattern(/^\d{3,3}-\d{3,3}-\d{4,4}$/)]

    });
  }

  addPost(post) {
    this.email = post.email;
    this.phone = post.phone;
    this.password = post.password;
  }
}
