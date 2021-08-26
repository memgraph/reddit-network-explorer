import { Component } from '@angular/core';
import { ApiService } from './services/api.service';

enum Event {
  CONNECT = 'connect',
  DISCONNECT = 'disconnect',
}

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  isConnected = false;

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.initIoConnection();
    this.api.data$.subscribe((data) => {
      console.log('got data', data);
    });
  }

  private initIoConnection(): void {
    this.api.initSocket();

    // This happens
    this.api.onEvent(Event.CONNECT).subscribe(() => {
      this.isConnected = true;
      console.log('connected');
    });

    this.api.onMessage().subscribe((message: any) => {
      console.log('Message', message);
    });

    this.api.onEvent(Event.DISCONNECT).subscribe(() => {
      this.isConnected = false;
      console.log('disconnected');
    });
  }
}
